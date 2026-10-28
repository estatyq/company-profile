"""Sixth pass: Forma — pick English in the visible modal, then capture landing + sandbox editor."""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        await ctx.add_init_script("localStorage.setItem('forma_lang', 'en');")
        page = await ctx.new_page()
        await page.goto("https://forma.ink/", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(6000)
        await page.screenshot(path=str(OUT / "forma_en_hero.png"))
        txt = await page.evaluate("document.body.innerText")
        (OUT / "forma_en.txt").write_text(txt, encoding="utf-8")
        for i, y in enumerate([900, 1800, 2700]):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(OUT / f"forma_en_s{i}.png"))
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(800)
        try:
            await page.evaluate("startSandbox()")
            await page.wait_for_timeout(5000)
            await page.screenshot(path=str(OUT / "forma_en_editor.png"))
            print("editor ok", flush=True)
        except Exception as e:  # noqa: BLE001
            print("sandbox failed", repr(e)[:200], flush=True)
        await browser.close()


asyncio.run(main())
