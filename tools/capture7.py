"""Seventh pass: Forma editor with a document open (English UI)."""
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
        await page.wait_for_timeout(5000)
        await page.evaluate("startSandbox()")
        await page.wait_for_timeout(4000)
        opened = False
        for sel in ["text=Resume - Template", "text=Resume – Template", "text=Cover Letter"]:
            loc = page.locator(sel).first
            if await loc.count():
                try:
                    await loc.click(timeout=4000)
                    await page.wait_for_timeout(5000)
                    opened = True
                    print("opened via", sel, flush=True)
                    break
                except Exception as e:  # noqa: BLE001
                    print("fail", sel, repr(e)[:150], flush=True)
        if not opened:
            # try first edit button inside cards
            btns = page.locator("button:has(svg)")
            print("buttons:", await btns.count(), flush=True)
        await page.screenshot(path=str(OUT / "forma_en_doc.png"))
        txt = await page.evaluate("document.body.innerText.slice(0, 3000)")
        (OUT / "forma_en_doc.txt").write_text(txt, encoding="utf-8")
        await browser.close()


asyncio.run(main())
