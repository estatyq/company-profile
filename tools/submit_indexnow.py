"""Notify IndexNow-compatible search engines about the public pages."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC_BASE_URL = os.getenv(
    "PUBLIC_BASE_URL", "https://xcombine.xyz"
).rstrip("/")


def indexnow_key() -> str:
    configured = os.getenv("INDEXNOW_KEY", "").strip()
    if configured:
        return configured
    markers = [
        path
        for path in (ROOT / "site").glob("*.txt")
        if re.fullmatch(r"[a-fA-F0-9]{32}\.txt", path.name)
    ]
    if len(markers) != 1:
        raise RuntimeError(
            "Expected exactly one 32-character IndexNow key file in site/"
        )
    return markers[0].stem


def public_urls() -> list[str]:
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(ROOT / "site" / "sitemap.xml")
    return [
        node.text.strip()
        for node in tree.findall(".//s:url/s:loc", namespace)
        if node.text and node.text.strip()
    ]


def submit(endpoint: str, urls: list[str]) -> None:
    key = indexnow_key()
    payload = json.dumps(
        {
            "host": "xcombine.xyz",
            "key": key,
            "keyLocation": f"{PUBLIC_BASE_URL}/{key}.txt",
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
