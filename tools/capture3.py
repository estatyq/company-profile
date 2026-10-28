"""Third pass: language switching, image inventory, extra views."""
import asyncio
import pathlib

from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"

IMGS_JS = """Array.from(document.querySelectorAll('img')).map(i => i.currentSrc + ' | ' + i.naturalWidth + 'x' + i.naturalHeight + ' | ' + (i.alt||'')).join('\\n')"""


async def new_page(browser):
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, locale="en-US")
    return ctx, await ctx.new_page()


async def rieltix(browser):
    ctx, page = await new_page(browser)
    await page.goto("https://rieltix.com/", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(5000)
    info = await page.evaluate(
        """(() => { const s = document.querySelector('select'); return s ? Array.from(s.options).map(o => o.value + '=' + o.text).join(', ') : 'no select'; })()"""
    )
    imgs = await page.evaluate(IMGS_JS)
    (OUT / "rieltix_imgs.txt").write_text(f"LANG: {info}\n\n{imgs}", encoding="utf-8")
    print("rieltix lang:", info, flush=True)
    try:
        sel = page.locator("select").first
        opts = await page.evaluate("Array.from(document.querySelector('select').options).map(o=>o.value)")
        en = next((o for o in opts if o.lower().startswith("en")), None)
        if en:
            await sel.select_option(en)
            await page.wait_for_timeout(4000)
            await page.screenshot(path=str(OUT / "rieltix_en_hero.png"))
            await page.screenshot(path=str(OUT / "rieltix_en_full.png"), full_page=True)
            txt = await page.evaluate("document.body.innerText")
            (OUT / "rieltix_en.txt").write_text(txt, encoding="utf-8")
            print("rieltix EN ok, url", page.url, flush=True)
    except Exception as e:  # noqa: BLE001
        print("rieltix EN failed", e, flush=True)
    await ctx.close()


async def forma(browser):
    ctx, page = await new_page(browser)
    await page.goto("https://forma.ink/", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(4000)
    try:
        await page.get_by_text("English", exact=True).first.click(timeout=5000)
        await page.wait_for_timeout(3000)
    except Exception as e:  # noqa: BLE001
        print("forma lang click failed", e, flush=True)
    await page.screenshot(path=str(OUT / "forma_en_hero.png"))
    await page.screenshot(path=str(OUT / "forma_en_full.png"), full_page=True)
    txt = await page.evaluate("document.body.innerText")
    imgs = await page.evaluate(IMGS_JS)
    (OUT / "forma_en.txt").write_text(txt + "\n\nIMGS:\n" + imgs, encoding="utf-8")
    print("forma EN ok", flush=True)
    await ctx.close()


async def mapest(browser):
    ctx, page = await new_page(browser)
    await page.goto("https://mapest.app/yak-tse-pratsiuye", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(6000)
    txt = await page.evaluate("document.body.innerText")
    (OUT / "mapest_how.txt").write_text(txt, encoding="utf-8")
    await page.screenshot(path=str(OUT / "mapest_how_hero.png"))
    print("mapest how ok", flush=True)
    await page.goto("https://mapest.app/?transaction=rent", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(8000)
    imgs = await page.evaluate(IMGS_JS)
    (OUT / "mapest_imgs.txt").write_text(imgs, encoding="utf-8")
    for label in ["МАПА", "КАРТА", "Карта"]:
        try:
            await page.get_by_text(label, exact=True).first.click(timeout=4000)
            await page.wait_for_timeout(7000)
            await page.screenshot(path=str(OUT / "mapest_map.png"))
            print("mapest map via", label, flush=True)
            break
        except Exception as e:  # noqa: BLE001
            print("mapest map click fail", label, str(e)[:120], flush=True)
    await ctx.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        for fn in (rieltix, forma, mapest):
            try:
                await fn(browser)
            except Exception as e:  # noqa: BLE001
                print(fn.__name__, "FAILED", e, flush=True)
        await browser.close()


asyncio.run(main())
