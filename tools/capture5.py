"""Fifth pass: Forma in English via changeLanguage, features + editor views."""
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
        page = await ctx.new_page()
        await page.goto("https://forma.ink/", wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(4000)
        try:
            await page.evaluate("changeLanguage('en')")
        except Exception as e:  # noqa: BLE001
            print("changeLanguage failed", repr(e)[:200], flush=True)
        await page.wait_for_timeout(2500)
        # close any modal leftovers
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(OUT / "forma_en_hero.png"))
        txt = await page.evaluate("document.body.innerText")
        (OUT / "forma_en.txt").write_text(txt, encoding="utf-8")
        btns = await page.evaluate(
            "Array.from(document.querySelectorAll('button, a')).filter(b => b.offsetParent).map(b => (b.innerText||'').trim().slice(0,40) + ' :: ' + (b.getAttribute('onclick')||'')).join('\\n')"
        )
        (OUT / "forma_en_buttons.txt").write_text(btns, encoding="utf-8")
        print("forma hero ok", flush=True)
        # scroll shots
        for i, y in enumerate([900, 1800, 2700]):
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(OUT / f"forma_en_s{i}.png"))
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(800)
        # open editor
        for label in ["Try for free", "Try it free", "Start for free", "Create"]:
            loc = page.get_by_text(label).first
            if await loc.count():
                try:
                    await loc.click(timeout=4000)
                    await page.wait_for_timeout(4000)
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(800)
                    await page.screenshot(path=str(OUT / "forma_en_editor.png"))
                    print("forma editor via", label, flush=True)
                    break
                except Exception as e:  # noqa: BLE001
                    print("editor fail", label, repr(e)[:120], flush=True)
        await browser.close()


asyncio.run(main())
