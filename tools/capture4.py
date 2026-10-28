"""Fourth pass: download Rieltix marketing shots, better Forma + Mapest views."""
import asyncio
import pathlib
import sys
import urllib.request

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "screens"

RIELTIX_IMGS = ["crm-properties.png", "public-site.png", "property-detail.png", "agents.png"]


def download_rieltix():
    for n in RIELTIX_IMGS:
        req = urllib.request.Request(f"https://rieltix.com/marketing/{n}", headers={"User-Agent": "Mozilla/5.0"})
        (OUT / f"rieltix_{n}").write_bytes(urllib.request.urlopen(req, timeout=30).read())
        print("downloaded", n, flush=True)
    req = urllib.request.Request("https://rieltix.com/rieltix-logo.svg", headers={"User-Agent": "Mozilla/5.0"})
    (OUT / "rieltix_logo.svg").write_bytes(urllib.request.urlopen(req, timeout=30).read())


async def forma(browser):
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, locale="en-US")
    page = await ctx.new_page()
    await page.goto("https://forma.ink/", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(4000)
    try:
        await page.locator("text=English").first.click(timeout=5000)
        await page.wait_for_timeout(3000)
    except Exception as e:  # noqa: BLE001
        print("forma lang click failed", repr(e)[:200], flush=True)
    await page.screenshot(path=str(OUT / "forma_en_hero.png"))
    txt = await page.evaluate("document.body.innerText")
    (OUT / "forma_en.txt").write_text(txt, encoding="utf-8")
    await page.screenshot(path=str(OUT / "forma_en_full.png"), full_page=True)
    print("forma EN hero/full ok", flush=True)
    # try open the editor
    for label in ["Try for free", "Start for free", "Get started"]:
        try:
            await page.get_by_text(label).first.click(timeout=4000)
            await page.wait_for_timeout(4000)
            await page.screenshot(path=str(OUT / "forma_en_editor.png"))
            print("forma editor via", label, flush=True)
            break
        except Exception as e:  # noqa: BLE001
            print("forma editor fail", label, repr(e)[:120], flush=True)
    await ctx.close()


async def mapest(browser):
    ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    page = await ctx.new_page()
    await page.goto("https://mapest.app/?transaction=rent", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(8000)
    # scroll to listing cards
    try:
        cards = page.get_by_text("СПИСОК", exact=True).last
        await cards.scroll_into_view_if_needed(timeout=5000)
        await page.mouse.wheel(0, 300)
        await page.wait_for_timeout(3000)
        await page.screenshot(path=str(OUT / "mapest_list.png"))
        print("mapest list ok", flush=True)
    except Exception as e:  # noqa: BLE001
        print("mapest list fail", repr(e)[:200], flush=True)
    # map, zoomed to a city
    try:
        await page.get_by_text("КАРТА", exact=True).last.click(timeout=5000)
        await page.wait_for_timeout(3000)
        await page.get_by_text("Харків", exact=True).last.click(timeout=5000)
        await page.wait_for_timeout(8000)
        mp = page.locator(".leaflet-container, .maplibregl-map, .mapboxgl-map").first
        await mp.scroll_into_view_if_needed(timeout=5000)
        await page.wait_for_timeout(3000)
        await page.screenshot(path=str(OUT / "mapest_map2.png"))
        print("mapest map2 ok", flush=True)
    except Exception as e:  # noqa: BLE001
        print("mapest map fail", repr(e)[:200], flush=True)
        await page.screenshot(path=str(OUT / "mapest_map2.png"))
    await ctx.close()
    # mobile
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
    page = await ctx.new_page()
    await page.goto("https://mapest.app/?transaction=rent", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(8000)
    await page.screenshot(path=str(OUT / "mapest_mobile.png"))
    print("mapest mobile ok", flush=True)
    await ctx.close()
    ctx = await browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
    page = await ctx.new_page()
    await page.goto("https://rieltix.com/", wait_until="domcontentloaded", timeout=45000)
    await page.wait_for_timeout(5000)
    await page.screenshot(path=str(OUT / "rieltix_mobile.png"))
    print("rieltix mobile ok", flush=True)
    await ctx.close()


async def main():
    try:
        download_rieltix()
    except Exception as e:  # noqa: BLE001
        print("rieltix download failed", repr(e)[:200], flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        for fn in (forma, mapest):
            try:
                await fn(browser)
            except Exception as e:  # noqa: BLE001
                print(fn.__name__, "FAILED", repr(e)[:300], flush=True)
        await browser.close()


asyncio.run(main())
