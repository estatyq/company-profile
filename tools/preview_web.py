"""Take screenshot of the generated web site viewer."""
import asyncio
import pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site" / "index.html"
OUT = ROOT / "output" / "preview" / "web_preview.png"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(SITE.as_uri(), wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(OUT))
        await browser.close()
        print("saved web preview")

asyncio.run(main())
