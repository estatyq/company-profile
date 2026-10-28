"""Validate generated SEO metadata, sitemap and crawler directives."""

from __future__ import annotations

import html.parser
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from build import LANGUAGES, PUBLIC_BASE_URL  # noqa: E402


class HeadParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.schema_blocks: list[str] = []
        self._in_schema = False
        self._schema_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key and values.get("content"):
                self.meta[key] = values["content"]
        elif tag == "link":
            self.links.append(values)
        elif tag == "script" and values.get("id") == "organization-schema":
            self._in_schema = True
            self._schema_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_schema:
            self._schema_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_schema:
            self.schema_blocks.append("".join(self._schema_parts))
            self._in_schema = False


def main() -> None:
    robots = (ROOT / "site" / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *" in robots
    assert "Allow: /" in robots
    assert f"Sitemap: {PUBLIC_BASE_URL}/sitemap.xml" in robots

    sitemap = ET.parse(ROOT / "site" / "sitemap.xml")
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = sitemap.findall(".//s:url/s:loc", namespace)
    assert len(urls) == len(LANGUAGES)

    expected_hreflang = set(LANGUAGES) | {"x-default"}
    for lang, meta in LANGUAGES.items():
        path = ROOT / "site" / meta["html"]
        parser = HeadParser()
        parser.feed(path.read_text(encoding="utf-8"))

        assert "index" in parser.meta.get("robots", "")
        assert parser.meta.get("og:image")
        assert parser.meta.get("og:image:width") == "1200"
        assert parser.meta.get("og:image:height") == "720"

        canonical = next(
            (link["href"] for link in parser.links if link.get("rel") == "canonical"),
            "",
        )
        expected_path = meta["html"] if lang != "en" else ""
        assert canonical == f"{PUBLIC_BASE_URL}/{expected_path}"

        hreflang = {
            link["hreflang"]
            for link in parser.links
            if link.get("rel") == "alternate" and link.get("hreflang")
        }
        assert hreflang == expected_hreflang

        assert len(parser.schema_blocks) == 1
        schema = json.loads(parser.schema_blocks[0])
        assert schema["@type"] == "ProfessionalService"
        assert schema["url"] == f"{PUBLIC_BASE_URL}/"
        assert schema["logo"].endswith("/assets/brand/xcombine-logo-color.png")
        assert schema["sameAs"]

    index_marker = re.compile(r"[a-f0-9]{32}\.txt$")
    markers = [
        path
        for path in (ROOT / "site").glob("*.txt")
        if index_marker.search(path.name)
    ]
    assert len(markers) == 1
    assert markers[0].read_text(encoding="utf-8").strip() == markers[0].stem

    print(
        f"SEO OK: {len(LANGUAGES)} language pages, canonical/hreflang/schema, "
        f"sitemap and IndexNow key"
    )


if __name__ == "__main__":
    main()
