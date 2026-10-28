"""End-to-end checks for /admin, persistence and authenticated uploads."""

from __future__ import annotations

import io
import json
import pathlib
import re
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app as application  # noqa: E402


def extract_csrf(html: str) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    if not match:
        raise AssertionError("CSRF token not found")
    return match.group(1)


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        temp = pathlib.Path(temporary)
        site = temp / "site"
        shutil.copytree(ROOT / "site", site)
        data = temp / "data"
        data.mkdir()
        application.DATA_DIR = data
        application.SITE_DIR = site
        application.UPLOAD_DIR = site / "assets" / "web" / "uploads"
        application.PROFILE_STORE = data / "profile.json"
        application.ADMIN_CREDENTIALS = data / "admin.json"
        application.SESSION_SECRET_FILE = data / ".session_secret"
        application.BACKUP_DIR = data / "backups"
        application.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        application.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        application.LOGIN_FAILURES.clear()
        application.app.config.update(TESTING=True, SECRET_KEY="test-secret")

        remote_client = application.app.test_client()
        remote_setup = remote_client.get(
            "/admin",
            environ_base={"REMOTE_ADDR": "203.0.113.20"},
        )
        assert remote_setup.status_code == 503
        assert "Настройте пароль на сервере" in remote_setup.get_data(as_text=True)

        client = application.app.test_client()
        response = client.get("/admin")
        assert response.status_code == 200
        assert "Создайте пароль администратора" in response.get_data(as_text=True)
        csrf = extract_csrf(response.get_data(as_text=True))

        response = client.post(
            "/admin/setup",
            data={
                "csrf_token": csrf,
                "password": "StrongTestPass!2026",
                "confirmation": "StrongTestPass!2026",
            },
        )
        assert response.status_code == 302

        response = client.get("/admin")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Управление профилем" in html
        bootstrap_match = re.search(
            r'<script id="admin-bootstrap" type="application/json">(.*?)</script>',
            html,
            re.S,
        )
        assert bootstrap_match
        bootstrap = json.loads(bootstrap_match.group(1))
        csrf = bootstrap["csrf"]
        content = bootstrap["content"]

        response = client.put(
            "/api/admin/content",
            json={
                "brand": "Test Studio",
                "contacts": {
                    "whatsapp": "+1 555 0100",
                    "telegram": "@test_studio",
                    "email": "hello@example.com",
                    "website": "example.com",
                },
                "languages": content["languages"],
            },
        )
        assert response.status_code == 400  # Missing CSRF must be rejected.

        content["brand"] = "Test Studio"
        content["contacts"]["email"] = "hello@example.com"
        content["languages"]["en"]["products"].append(
            {
                "id": "new-project",
                "name": "New Project",
                "url": "https://example.com",
                "shot": "",
                "coverSub": "Web product",
                "status": "Live",
                "tag": "A new portfolio project",
                "features": ["Feature one", "Feature two"],
                "benefit": "Less manual work.",
                "badgeColor": "m",
            }
        )
        content["languages"]["en"]["text"]["cover_title_a"] = (
            "Designed for growing teams"
        )
        response = client.put(
            "/api/admin/content",
            json=content,
            headers={"X-CSRF-Token": csrf},
        )
        assert response.status_code == 200, response.get_data(as_text=True)
        content = response.get_json()["content"]

        logo = io.BytesIO(
            (ROOT / "assets" / "web" / "forma_doc.jpg").read_bytes()
        )
        response = client.post(
            "/api/admin/logo",
            data={"logo": (logo, "logo.png")},
            headers={"X-CSRF-Token": csrf},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200, response.get_data(as_text=True)
        logo_path = response.get_json()["logo"]
        assert logo_path.endswith(".png")
        assert (site / "assets" / "web" / logo_path).exists()
        content["logo"] = logo_path
        response = client.put(
            "/api/admin/content",
            json=content,
            headers={"X-CSRF-Token": csrf},
        )
        assert response.status_code == 200

        profile = json.loads((site / "profile-en.json").read_text(encoding="utf-8"))
        assert profile["brand"] == "Test Studio"
        assert profile["logo"] == logo_path
        assert profile["contacts"]["email"] == "hello@example.com"
        assert any(product["id"] == "new-project" for product in profile["products"])
        assert profile["text"]["cover_title_a"] == "Designed for growing teams"
        assert application.PROFILE_STORE.exists()

        image = io.BytesIO((ROOT / "assets" / "web" / "rieltix_site.jpg").read_bytes())
        response = client.post(
            "/api/admin/upload",
            data={"image": (image, "project.jpg")},
            headers={"X-CSRF-Token": csrf},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200, response.get_data(as_text=True)
        uploaded = response.get_json()["shot"]
        assert (site / "assets" / "web" / uploaded).exists()

        assert client.get("/").status_code == 200
        assert client.get("/id.html").status_code == 200
        assert client.get("/assets/app.js").status_code == 200
        assert client.get("/profile-en.json").get_json()["brand"] == "Test Studio"
        manifest = client.get("/assets/site.webmanifest").get_json()
        assert manifest["name"] == "Test Studio"
        assert manifest["icons"][0]["src"].endswith(".png")
        robots = client.get("/robots.txt").get_data(as_text=True)
        assert "Sitemap: https://xcombine.xyz/sitemap.xml" in robots
        assert client.get("/sitemap.xml").status_code == 200

        response = client.post(
            "/admin/logout",
            data={"csrf_token": csrf},
        )
        assert response.status_code == 302
        assert client.get("/api/admin/content").status_code == 401

        anonymous = application.app.test_client()
        response = anonymous.get("/admin")
        assert response.status_code == 200
        assert "Вход в панель управления" in response.get_data(as_text=True)

    print("Admin OK: setup, auth, CSRF, save, upload, public files, logout")


if __name__ == "__main__":
    main()
