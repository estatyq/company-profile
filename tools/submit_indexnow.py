"""Notify IndexNow-compatible search engines about the public pages."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from build import INDEXNOW_KEY, PUBLIC_BASE_URL  # noqa: E402


def public_urls() -> list[str]:
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(ROOT / "site" / "sitemap.xml")
    return [
        node.text.strip()
        for node in tree.findall(".//s:url/s:loc", namespace)
        if node.text and node.text.strip()
    ]


def submit(endpoint: str, urls: list[str]) -> None:
    payload = json.dumps(
        {
            "host": "xcombine.xyz",
            "key": INDEXNOW_KEY,
            "keyLocation": f"{PUBLIC_BASE_URL}/{INDEXNOW_KEY}.txt",
            "urlList": urls,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "XCOMBINE-IndexNow/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        print(f"{endpoint}: HTTP {response.status}, {len(urls)} URLs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        default="https://api.indexnow.org/indexnow",
        help="IndexNow API endpoint",
    )
    args = parser.parse_args()
    urls = public_urls()
    if not urls:
        raise RuntimeError("No public URLs found in site/sitemap.xml")
    try:
        submit(args.endpoint, urls)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"IndexNow rejected the request: HTTP {error.code}: {body}"
        ) from error


if __name__ == "__main__":
    main()
