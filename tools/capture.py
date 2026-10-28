"""Capture screenshots and visible text of the real project websites."""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"
OUT.mkdir(parents=True, exist_ok=True)

SITES = {
    "rieltix": "https://rieltix.com/",
    "mapest": "https://mapest.app/",
    "forma": "https://forma.ink/",
}


async def grab(browser, name, url):
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    page = await ctx.new_page()
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
    except Exception as e:  # noqa: BLE001
        print(f"[{name}] goto warning: {e}", file=sys.stderr)
    await page.wait_for_timeout(4000)
    await page.screenshot(path=str(OUT / f"{name}_hero.png"))
    await page.screenshot(path=str(OUT / f"{name}_full.png"), full_page=True)
    text = await page.evaluate("document.body.innerText")
    links = await page.evaluate(
        "Array.from(document.querySelectorAll('a')).map(a => a.innerText.trim() + ' -> ' + a.href).join('\\n')"
    )
    title = await page.title()
    (OUT / f"{name}.txt").write_text(f"TITLE: {title}\nURL: {page.url}\n\n{text}\n\nLINKS:\n{links}", encoding="utf-8")
    print(f"[{name}] ok: {title} ({page.url})")
    await ctx.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        for name, url in SITES.items():
            try:
                await grab(browser, name, url)
            except Exception as e:  # noqa: BLE001
                print(f"[{name}] FAILED: {e}")
        await browser.close()


asyncio.run(main())
