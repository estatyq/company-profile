"""Protected admin and persistent content for the Company Profile website."""

from __future__ import annotations

import functools
import hmac
import io
import ipaddress
import json
import os
import pathlib
import re
import secrets
import shutil
import threading
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

from content import (
    BRAND_NAME,
    CONTACTS,
    LANGUAGES as LANGUAGE_META,
    PRODUCTS,
    language_text,
    product_text,
)


ROOT = pathlib.Path(__file__).resolve().parent
SITE_DIR = ROOT / "site"
DATA_DIR = ROOT / "data"
UPLOAD_DIR = SITE_DIR / "assets" / "web" / "uploads"
PROFILE_STORE = DATA_DIR / "profile.json"
ADMIN_CREDENTIALS = DATA_DIR / "admin.json"
SESSION_SECRET_FILE = DATA_DIR / ".session_secret"
BACKUP_DIR = DATA_DIR / "backups"

TEXT_FIELDS = (
    "cover_chip",
    "cover_eyebrow",
    "cover_title_a",
    "cover_title_b",
    "cover_sub",
    "cover_lead",
    "cover_products_label",
    "p2_eyebrow",
    "p2_title_a",
    "p2_title_b",
    "p2_lead",
    "p2_problems_label",
    "p2_flow_label",
    "p2_cmp_label",
    "p3_eyebrow",
    "p3_title",
    "p3_title_continued",
    "p3_lead",
    "benefit_label",
    "p4_eyebrow",
    "p4_title",
    "p4_lead",
    "example_label",
    "p5_eyebrow",
    "p5_title_a",
    "p5_title_b",
    "p5_lead",
    "p5_phases_label",
    "p6_eyebrow",
    "p6_title",
    "models_label",
    "cta_a",
    "cta_b",
    "cta_note",
)
CONTACT_FIELDS = ("whatsapp", "telegram", "email", "website")
LANGUAGES = tuple(LANGUAGE_META.keys())
WRITE_LOCK = threading.RLock()
LOGIN_FAILURES: dict[str, list[float]] = {}
LOGIN_WINDOW_SECONDS = 10 * 60
LOGIN_MAX_FAILURES = 5
MAX_ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")


def _load_dotenv() -> None:
    """Load a simple KEY=VALUE .env file without evaluating shell syntax."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            os.environ.setdefault(key, value)


_load_dotenv()


def _ensure_directories() -> None:
    for path in (DATA_DIR, UPLOAD_DIR, BACKUP_DIR):
        path.mkdir(parents=True, exist_ok=True)


def _load_session_secret() -> str:
    configured = os.getenv("SECRET_KEY", "").strip()
    if configured:
        return configured
    if SESSION_SECRET_FILE.exists():
        return SESSION_SECRET_FILE.read_text(encoding="utf-8").strip()
    secret = secrets.token_urlsafe(48)
    SESSION_SECRET_FILE.write_text(secret, encoding="utf-8")
    return secret


_ensure_directories()
app = Flask(__name__, static_folder=None)
app.config.update(
    SECRET_KEY=_load_session_secret(),
    MAX_CONTENT_LENGTH=12 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
)
if os.getenv("TRUST_PROXY", "0") == "1":
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1,
    )


def _default_products(lang: str) -> list[dict]:
    result = []
    for product in PRODUCTS:
        result.append(
            {
                "id": product["id"],
                "name": product["name"],
                "url": product["url"],
                "shot": product.get("shot", ""),
                "coverSub": product_text(product, "cover_sub", lang),
                "status": product_text(product, "status", lang) or "Live",
                "tag": product_text(product, "tag", lang),
                "features": list(product_text(product, "features", lang)),
                "benefit": product_text(product, "benefit", lang),
                "badgeColor": product.get("badge_color", "r"),
            }
        )
    return result


def _default_store() -> dict:
    english = language_text("en")
    return {
        "version": 2,
        "brand": BRAND_NAME or english["descriptor"],
        "logo": "",
        "contacts": {key: CONTACTS.get(key, "") for key in CONTACT_FIELDS},
        "languages": {
            lang: {
                "products": _default_products(lang),
                "text": {
                    key: language_text(lang).get(key, "")
                    for key in TEXT_FIELDS
                },
            }
            for lang in LANGUAGES
        },
    }


def _merge_language_file(store: dict, lang: str) -> None:
    path = SITE_DIR / f"profile-{lang}.json"
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    if not isinstance(data, dict):
        return
    if isinstance(data.get("brand"), str):
        store["brand"] = data["brand"]
    if isinstance(data.get("logo"), str) and data["logo"]:
        store["logo"] = data["logo"]
    if isinstance(data.get("contacts"), dict):
        for key in CONTACT_FIELDS:
            value = data["contacts"].get(key)
            if isinstance(value, str):
                store["contacts"][key] = value
    if isinstance(data.get("products"), list):
        store["languages"][lang]["products"] = data["products"]
    if isinstance(data.get("text"), dict):
        store["languages"][lang]["text"].update(
            {
                key: value
                for key, value in data["text"].items()
                if key in TEXT_FIELDS and isinstance(value, str)
            }
        )


def load_store() -> dict:
    with WRITE_LOCK:
        if PROFILE_STORE.exists():
            try:
                raw = json.loads(PROFILE_STORE.read_text(encoding="utf-8"))
                return normalize_store(raw)
            except (OSError, ValueError, json.JSONDecodeError):
                backup = BACKUP_DIR / f"profile-invalid-{int(time.time())}.json"
                shutil.copy2(PROFILE_STORE, backup)
        store = _default_store()
        for lang in LANGUAGES:
            _merge_language_file(store, lang)
        return normalize_store(store)


def _text(value, limit: int) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError("Expected text")
    value = value.replace("\x00", "").strip()
    if len(value) > limit:
        raise ValueError(f"Text exceeds {limit} characters")
    return value


def _url(value) -> str:
    value = _text(value, 500)
    if not value:
        return ""
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Links must start with http:// or https://")
    return value


def _shot(value) -> str:
    value = _text(value, 300).replace("\\", "/")
    if not value:
        return ""
    if value.startswith("/") or ".." in value.split("/"):
        raise ValueError("Invalid image path")
    return value


def _normalize_product(raw: dict, index: int, lang: str) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("Each project must be an object")
    product_id = _text(raw.get("id"), 80)
    if not MAX_ID.fullmatch(product_id):
        product_id = f"{lang}-project-{uuid.uuid4().hex[:12]}"
    features = raw.get("features", [])
    if isinstance(features, str):
        features = features.splitlines()
    if not isinstance(features, list):
        raise ValueError("Project features must be a list")
    clean_features = [
        _text(feature, 240) for feature in features[:12] if _text(feature, 240)
    ]
    badge_color = raw.get("badgeColor", "r")
    if badge_color not in ("r", "m", "f"):
        badge_color = "r"
    return {
        "id": product_id,
        "name": _text(raw.get("name"), 80) or f"Project {index + 1}",
        "url": _url(raw.get("url")),
        "shot": _shot(raw.get("shot")),
        "coverSub": _text(raw.get("coverSub"), 100),
        "status": _text(raw.get("status"), 40) or "Live",
        "tag": _text(raw.get("tag"), 180),
        "features": clean_features,
        "benefit": _text(raw.get("benefit"), 500),
        "badgeColor": badge_color,
    }


def normalize_store(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("Invalid profile data")
    defaults = _default_store()
    contacts = raw.get("contacts") if isinstance(raw.get("contacts"), dict) else {}
    languages = raw.get("languages") if isinstance(raw.get("languages"), dict) else {}
    result = {
        "version": 2,
        "brand": _text(raw.get("brand"), 90) or defaults["brand"],
        "logo": _shot(raw.get("logo")),
        "contacts": {
            key: _text(contacts.get(key), 250) for key in CONTACT_FIELDS
        },
        "languages": {},
    }
    for lang in LANGUAGES:
        raw_language = (
            languages.get(lang) if isinstance(languages.get(lang), dict) else {}
        )
        products = raw_language.get("products")
        if not isinstance(products, list):
            products = defaults["languages"][lang]["products"]
        if len(products) > 100:
            raise ValueError("A maximum of 100 projects is allowed")
        seen_ids = set()
        normalized_products = []
        for index, product in enumerate(products):
            clean_product = _normalize_product(product, index, lang)
            if clean_product["id"] in seen_ids:
                clean_product["id"] = f"{lang}-project-{uuid.uuid4().hex[:12]}"
            seen_ids.add(clean_product["id"])
            normalized_products.append(clean_product)
        raw_text = (
            raw_language.get("text")
            if isinstance(raw_language.get("text"), dict)
            else {}
        )
        text = {}
        for key in TEXT_FIELDS:
            fallback = defaults["languages"][lang]["text"].get(key, "")
            value = raw_text.get(key, fallback)
            text[key] = _text(value, 1200 if key.endswith("_lead") else 300)
        result["languages"][lang] = {
            "products": normalized_products,
            "text": text,
        }
    return result


def _atomic_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _backup_current_store() -> None:
    if not PROFILE_STORE.exists():
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    shutil.copy2(PROFILE_STORE, BACKUP_DIR / f"profile-{stamp}.json")
    backups = sorted(BACKUP_DIR.glob("profile-*.json"), reverse=True)
    for old_backup in backups[20:]:
        old_backup.unlink(missing_ok=True)


def save_store(store: dict) -> None:
    normalized = normalize_store(store)
    with WRITE_LOCK:
        _backup_current_store()
        _atomic_json(PROFILE_STORE, normalized)
        for lang in LANGUAGES:
            language = normalized["languages"][lang]
            public = {
                "version": 2,
                "lang": lang,
                "brand": normalized["brand"],
                "logo": normalized["logo"],
                "contacts": normalized["contacts"],
                "products": language["products"],
                "text": language["text"],
            }
            _atomic_json(SITE_DIR / f"profile-{lang}.json", public)


def _credentials_configured() -> bool:
    return bool(os.getenv("ADMIN_PASSWORD", "").strip()) or ADMIN_CREDENTIALS.exists()


def _is_local_request() -> bool:
    try:
        return ipaddress.ip_address(request.remote_addr or "").is_loopback
    except ValueError:
        return False


def _password_matches(password: str) -> bool:
    configured = os.getenv("ADMIN_PASSWORD", "").strip()
    if configured:
        return hmac.compare_digest(password, configured)
    try:
        data = json.loads(ADMIN_CREDENTIALS.read_text(encoding="utf-8"))
        password_hash = data.get("password_hash", "")
        return bool(password_hash) and check_password_hash(password_hash, password)
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def _login_allowed(client: str) -> bool:
    now = time.monotonic()
    recent = [
        stamp
        for stamp in LOGIN_FAILURES.get(client, [])
        if now - stamp < LOGIN_WINDOW_SECONDS
    ]
    LOGIN_FAILURES[client] = recent
    return len(recent) < LOGIN_MAX_FAILURES


def _record_login_failure(client: str) -> None:
    LOGIN_FAILURES.setdefault(client, []).append(time.monotonic())


def _csrf_token() -> str:
    token = session.get("_csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf"] = token
    return token


def _check_csrf() -> None:
    expected = session.get("_csrf", "")
    supplied = request.headers.get("X-CSRF-Token") or request.form.get(
        "csrf_token", ""
    )
    if not expected or not supplied or not hmac.compare_digest(expected, supplied):
        abort(400, description="Invalid CSRF token")


def _is_admin() -> bool:
    return bool(session.get("admin_authenticated"))


def admin_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if not _is_admin():
            if request.path.startswith("/api/"):
                return jsonify({"error": "Authentication required"}), 401
            return redirect(url_for("admin"))
        return view(*args, **kwargs)

    return wrapped


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; "
        "connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    )
    if request.path.startswith("/admin") or request.path.startswith("/api/admin"):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.before_request
def protect_write_requests():
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        if request.path.startswith("/admin") or request.path.startswith("/api/admin"):
            _check_csrf()


@app.get("/admin", strict_slashes=False)
def admin():
    if not _credentials_configured():
        if not _is_local_request():
            return render_template(
                "admin_auth.html",
                mode="unavailable",
                csrf_token=_csrf_token(),
                error=None,
            ), 503
        return render_template(
            "admin_auth.html",
            mode="setup",
            csrf_token=_csrf_token(),
            error=None,
        )
    if not _is_admin():
        return render_template(
            "admin_auth.html",
            mode="login",
            csrf_token=_csrf_token(),
            error=request.args.get("error"),
        )
    content = load_store()
    bootstrap = {
        "content": content,
        "csrf": _csrf_token(),
        "environmentPassword": bool(os.getenv("ADMIN_PASSWORD", "").strip()),
        "languages": [
            {"code": code, **meta} for code, meta in LANGUAGE_META.items()
        ],
    }
    serialized = json.dumps(bootstrap, ensure_ascii=False).replace("</", "<\\/")
    return render_template(
        "admin.html",
        bootstrap_json=serialized,
        csrf_token=_csrf_token(),
    )


@app.post("/admin/setup")
def admin_setup():
    if _credentials_configured() or not _is_local_request():
        return redirect(url_for("admin"))
    password = request.form.get("password", "")
    confirmation = request.form.get("confirmation", "")
    if len(password) < 10:
        return render_template(
            "admin_auth.html",
            mode="setup",
            csrf_token=_csrf_token(),
            error="Пароль должен содержать минимум 10 символов.",
        ), 400
    if password != confirmation:
        return render_template(
            "admin_auth.html",
            mode="setup",
            csrf_token=_csrf_token(),
            error="Пароли не совпадают.",
        ), 400
    _atomic_json(
        ADMIN_CREDENTIALS,
        {"password_hash": generate_password_hash(password, method="scrypt")},
    )
    session.clear()
    session["admin_authenticated"] = True
    session.permanent = True
    _csrf_token()
    return redirect(url_for("admin"))


@app.post("/admin/login")
def admin_login():
    client = request.remote_addr or "unknown"
    if not _login_allowed(client):
        return render_template(
            "admin_auth.html",
            mode="login",
            csrf_token=_csrf_token(),
            error="Слишком много попыток. Повторите вход через 10 минут.",
        ), 429
    if not _password_matches(request.form.get("password", "")):
        _record_login_failure(client)
        return render_template(
            "admin_auth.html",
            mode="login",
            csrf_token=_csrf_token(),
            error="Неверный пароль.",
        ), 401
    session.clear()
    session["admin_authenticated"] = True
    session.permanent = True
    _csrf_token()
    return redirect(url_for("admin"))


@app.post("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("admin"))


@app.get("/api/admin/content")
@admin_required
def get_admin_content():
    return jsonify(load_store())


@app.put("/api/admin/content")
@admin_required
def update_admin_content():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid JSON"}), 400
    try:
        normalized = normalize_store(payload)
        save_store(normalized)
    except ValueError as error:
        return jsonify({"error": str(error)}), 422
    return jsonify({"ok": True, "content": normalized})


@app.post("/api/admin/upload")
@admin_required
def upload_image():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "Image is required"}), 400
    try:
        raw = file.read()
        if not raw or len(raw) > 10 * 1024 * 1024:
            raise ValueError("Image must be smaller than 10 MB")
        Image.MAX_IMAGE_PIXELS = 30_000_000
        image = Image.open(io.BytesIO(raw))
        image.verify()
        image = Image.open(io.BytesIO(raw))
        image = ImageOps.exif_transpose(image).convert("RGB")
        image.thumbnail((1600, 1000), Image.Resampling.LANCZOS)
        filename = f"{uuid.uuid4().hex}.jpg"
        destination = UPLOAD_DIR / filename
        image.save(destination, "JPEG", quality=84, optimize=True, progressive=True)
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify({"error": "Upload a valid JPG, PNG or WebP image"}), 422
    return jsonify({"ok": True, "shot": f"uploads/{filename}"})


@app.post("/api/admin/logo")
@admin_required
def upload_logo():
    file = request.files.get("logo")
    if not file:
        return jsonify({"error": "Logo is required"}), 400
    try:
        raw = file.read()
        if not raw or len(raw) > 5 * 1024 * 1024:
            raise ValueError("Logo must be smaller than 5 MB")
        Image.MAX_IMAGE_PIXELS = 30_000_000
        source = Image.open(io.BytesIO(raw))
        source.verify()
        source = Image.open(io.BytesIO(raw))
        image = ImageOps.exif_transpose(source)
        if image.mode not in ("RGBA", "LA"):
            image = image.convert("RGBA")
        image.thumbnail((800, 400), Image.Resampling.LANCZOS)
        filename = f"logo-{uuid.uuid4().hex}.png"
        destination = UPLOAD_DIR / filename
        image.save(destination, "PNG", optimize=True)
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify({"error": "Upload a valid PNG, JPG or WebP logo"}), 422
    return jsonify({"ok": True, "logo": f"uploads/{filename}"})


@app.post("/api/admin/password")
@admin_required
def change_password():
    if os.getenv("ADMIN_PASSWORD", "").strip():
        return jsonify(
            {"error": "Пароль задаётся переменной окружения ADMIN_PASSWORD."}
        ), 403
    payload = request.get_json(silent=True) or {}
    current = str(payload.get("current", ""))
    new_password = str(payload.get("new", ""))
    if not _password_matches(current):
        return jsonify({"error": "Текущий пароль указан неверно."}), 401
    if len(new_password) < 10:
        return jsonify({"error": "Новый пароль должен быть не короче 10 символов."}), 422
    _atomic_json(
        ADMIN_CREDENTIALS,
        {"password_hash": generate_password_hash(new_password, method="scrypt")},
    )
    return jsonify({"ok": True})


@app.get("/admin-static/<path:filename>")
def admin_static(filename: str):
    return send_from_directory(ROOT / "admin_static", filename)


@app.get("/")
def index():
    return send_from_directory(SITE_DIR, "index.html")


@app.get("/profile-<lang>.json")
def public_profile(lang: str):
    if lang not in LANGUAGES:
        abort(404)
    store = load_store()
    language = store["languages"][lang]
    return jsonify(
        {
            "version": 2,
            "lang": lang,
            "brand": store["brand"],
            "logo": store["logo"],
            "contacts": store["contacts"],
            "products": language["products"],
            "text": language["text"],
        }
    )


@app.get("/assets/site.webmanifest")
def site_manifest():
    store = load_store()
    logo = (
        f"/assets/web/{store['logo']}"
        if store.get("logo")
        else "/assets/favicon.svg"
    )
    return jsonify(
        {
            "name": store["brand"],
            "short_name": store["brand"][:24],
            "start_url": "/",
            "display": "standalone",
            "background_color": "#05080f",
            "theme_color": "#05080f",
            "icons": [
                {
                    "src": logo,
                    "sizes": "any",
                    "type": "image/png" if store.get("logo") else "image/svg+xml",
                    "purpose": "any",
                }
            ],
        }
    )


@app.get("/<path:filename>")
def site_file(filename: str):
    candidate = (SITE_DIR / filename).resolve()
    try:
        candidate.relative_to(SITE_DIR.resolve())
    except ValueError:
        abort(404)
    if not candidate.is_file():
        abort(404)
    return send_from_directory(candidate.parent, candidate.name)


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Файл слишком большой. Максимум 10 МБ."}), 413


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8765"))
    app.run(host=host, port=port, debug=False)
