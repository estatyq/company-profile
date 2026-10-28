"""Validate language registry, translations and product localization."""

from __future__ import annotations

import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from content import LANGUAGES, PRODUCTS, language_text  # noqa: E402


def main() -> None:
    problems = []
    required_language_fields = {"label", "native", "html", "file_suffix"}
    html_names = set()
    english_keys = set(language_text("en"))
    for code, meta in LANGUAGES.items():
        missing_meta = required_language_fields - set(meta)
        if missing_meta:
            problems.append(f"{code}: missing language metadata {sorted(missing_meta)}")
        if meta.get("html") in html_names:
            problems.append(f"{code}: duplicate html file {meta.get('html')}")
        html_names.add(meta.get("html"))
        missing_text = english_keys - set(language_text(code))
        if missing_text:
            problems.append(f"{code}: missing text keys {sorted(missing_text)}")
        for product in PRODUCTS:
            for key in ("status", "cover_sub", "tag", "features", "benefit"):
                localized = product.get(key, {})
                if isinstance(localized, dict) and code not in localized:
                    problems.append(
                        f"{code}/{product['id']}: no translation for '{key}' "
                        "(English fallback will be used)"
                    )
    if problems:
        print("\n".join(f"- {problem}" for problem in problems))
        raise SystemExit(1)
    print(f"Languages OK: {len(LANGUAGES)} languages, {len(PRODUCTS)} products")


if __name__ == "__main__":
    main()
