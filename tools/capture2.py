"""Second pass: robust capture with domcontentloaded, language exploration."""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = sys.argv[1:] or ["forma=https://forma.ink/", "mapest=https://mapest.app/"]


async def grab(browser, name, url, full=True):
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, locale="en-US")
    page = await ctx.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:  # noqa: BLE001
        print(f"[{name}] goto warning: {e}")
    await page.wait_for_timeout(7000)
    await page.screenshot(path=str(OUT / f"{name}_hero.png"), timeout=30000)
    print(f"[{name}] hero saved", flush=True)
    text = await page.evaluate("document.body.innerText")
    links = await page.evaluate(
        "Array.from(document.querySelectorAll('a')).map(a => (a.innerText||'').trim().slice(0,60) + ' -> ' + a.href).join('\\n')"
    )
    langs = await page.evaluate(
        "Array.from(document.querySelectorAll('select option, [hreflang], button')).map(e => (e.getAttribute('hreflang')||'') + ' ' + (e.value||'') + ' ' + (e.innerText||'').trim().slice(0,30)).join(' | ')"
    )
    title = await page.title()
    (OUT / f"{name}.txt").write_text(
        f"TITLE: {title}\nURL: {page.url}\n\n{text}\n\nLINKS:\n{links}\n\nLANG/BUTTONS:\n{langs}", encoding="utf-8"
    )
    print(f"[{name}] text saved: {title} ({page.url})", flush=True)
    if full:
        try:
            await page.screenshot(path=str(OUT / f"{name}_full.png"), full_page=True, timeout=60000)
            print(f"[{name}] full saved", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"[{name}] full failed: {e}", flush=True)
    await ctx.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        for t in TARGETS:
            name, url = t.split("=", 1)
            try:
                await grab(browser, name, url)
            except Exception as e:  # noqa: BLE001
                print(f"[{name}] FAILED: {e}", flush=True)
        await browser.close()


asyncio.run(main())
