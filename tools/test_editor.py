"""Smoke-test the interactive editor and its browser exports."""

import asyncio
import functools
import http.server
import pathlib
import threading

import fitz
from playwright.async_api import async_playwright


ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site" / "index.html"
PREVIEW = ROOT / "output" / "preview"
QA_DOCX = ROOT / "output" / "interactive_editor_qa.docx"
QA_PDF = ROOT / "output" / "interactive_editor_qa.pdf"
STATIC_PDF = ROOT / "output" / "downloaded_profile.pdf"


async def main():
    PREVIEW.mkdir(parents=True, exist_ok=True)
    errors = []
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, _format, *args):
            pass

    handler = functools.partial(QuietHandler, directory=str(ROOT / "site"))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    site_url = f"http://127.0.0.1:{server.server_port}/index.html"
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            accept_downloads=True,
        )
        page = await context.new_page()
        await page.add_init_script(
            "localStorage.setItem('company-profile-language-selection', 'en')"
        )
        page.on(
            "console",
            lambda message: errors.append(f"console:{message.type}:{message.text}")
            if message.type == "error"
            else None,
        )
        page.on("pageerror", lambda error: errors.append(f"pageerror:{error}"))
        await page.goto(SITE.as_uri(), wait_until="networkidle")
        await page.evaluate("localStorage.removeItem('company-profile-builder-v1')")
        await page.reload(wait_until="networkidle")

        assert await page.locator(".deck-container .page").count() == 6
        await page.evaluate("window.profileEditor.open()")
        await page.locator("#editor-brand").fill("Студия Север")
        await page.locator("#editor-whatsapp").fill("+7 978 123-45-67")
        await page.locator("#editor-telegram").fill("@north_studio")
        await page.locator("#editor-email").fill("hello@example.com")
        await page.locator("#add-project").click()

        product = page.locator(".product-editor").last
        await product.locator('[data-field="name"]').fill("Новый продукт")
        await product.locator('[data-field="url"]').fill("https://example.com")
        await product.locator('[data-field="coverSub"]').fill("Digital product")
        await product.locator('[data-field="tag"]').fill("Operations platform")
        await product.locator('[data-field="features"]').fill(
            "Client portal\nAutomated workflow"
        )
        await product.locator('[data-field="benefit"]').fill(
            "Сокращает ручную работу команды."
        )
        await product.locator('[data-image-upload]').set_input_files(
            ROOT / "assets" / "web" / "rieltix_site.jpg"
        )
        await page.wait_for_function(
            """() => document.querySelector(
                '.product-editor[open] .image-preview img'
            )?.src.startsWith('data:image/jpeg')"""
        )
        await page.screenshot(path=str(PREVIEW / "editor_preview.png"))
        await page.locator("#save-profile").click()

        assert await page.locator(".deck-container .page").count() == 7
        assert (
            await page.locator(".mark span").first.text_content()
        ).strip() == "Студия Север"
        assert await page.locator(".p3").count() == 2
        assert await page.get_by_text("Новый продукт", exact=True).count() >= 1
        assert await page.locator(".p3 .prod img").count() == 4
        footer = page.locator(".web-footer")
        await footer.scroll_into_view_if_needed()
        assert await page.locator(".footer-action").count() == 2
        icon_box = await page.locator("#download-pdf .footer-action-icon svg").bounding_box()
        assert icon_box and icon_box["width"] <= 18 and icon_box["height"] <= 18
        footer_background = await page.locator("#download-pdf").evaluate(
            "element => getComputedStyle(element).backgroundColor"
        )
        assert footer_background != "rgb(255, 255, 255)"
        assert await page.locator("#edit-profile").count() == 0
        await page.reload(wait_until="networkidle")
        assert (
            await page.locator(".mark span").first.text_content()
        ).strip() == "Студия Север"
        assert await page.locator(".deck-container .page").count() == 7

        async with page.expect_download(timeout=30000) as download_info:
            await page.locator("#download-word").click()
        download = await download_info.value
        await download.save_as(QA_DOCX)
        assert QA_DOCX.stat().st_size > 8000

        await page.pdf(
            path=str(QA_PDF),
            width="1280px",
            height="720px",
            print_background=True,
            prefer_css_page_size=True,
        )
        with fitz.open(QA_PDF) as document:
            assert document.page_count == 7

        await page.screenshot(path=str(PREVIEW / "editor_saved_site.png"))

        published_context = await browser.new_context(viewport={"width": 1440, "height": 900})
        published_page = await published_context.new_page()
        await published_page.add_init_script(
            "localStorage.setItem('company-profile-language-selection', 'en')"
        )
        await published_page.route(
            "**/profile-en.json",
            lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body='{"version":1,"lang":"en","brand":"Published Studio",'
                '"contacts":{"email":"published@example.com"},'
                '"products":[{"id":"published","name":"Published Work",'
                '"url":"https://example.com","shot":"","coverSub":"Web product",'
                '"status":"Live","tag":"A published portfolio item",'
                '"features":["One"],"benefit":"A clear result",'
                '"badgeColor":"r","imageData":""}]}',
            ),
        )
        await published_page.goto(site_url, wait_until="networkidle")
        await published_page.wait_for_function(
            "document.querySelector('.mark .brand-name')?.textContent === 'Published Studio'"
        )
        assert (
            await published_page.locator(".mark .brand-name").first.text_content()
        ).strip() == "Published Studio"
        assert await published_page.get_by_text("Published Work", exact=True).count() >= 1
        async with published_page.expect_download(
            timeout=30000
        ) as pdf_download_info:
            await published_page.locator("#download-pdf").click()
        pdf_download = await pdf_download_info.value
        await pdf_download.save_as(STATIC_PDF)
        assert STATIC_PDF.read_bytes().startswith(b"%PDF")
        assert STATIC_PDF.stat().st_size > 100000
        await published_context.close()

        mobile_context = await browser.new_context(
            viewport={"width": 390, "height": 844}
        )
        mobile_page = await mobile_context.new_page()
        await mobile_page.add_init_script(
            "localStorage.setItem('company-profile-language-selection', 'en')"
        )
        await mobile_page.goto(site_url, wait_until="networkidle")
        assert await mobile_page.locator(".deck-container .page").count() == 6
        assert not await mobile_page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        menu_font_size = await mobile_page.locator(".site-nav a").first.evaluate(
            "element => parseFloat(getComputedStyle(element).fontSize)"
        )
        assert menu_font_size >= 11.5
        await mobile_page.locator('.site-nav a[href="#products"]').click()
        target_top = await mobile_page.locator("#products").evaluate(
            "element => element.getBoundingClientRect().top"
        )
        header_bottom = await mobile_page.locator(".web-header").evaluate(
            "element => element.getBoundingClientRect().bottom"
        )
        assert target_top > header_bottom + 20
        await mobile_context.close()
        await browser.close()
    server.shutdown()
    server_thread.join(timeout=3)

    if errors:
        raise RuntimeError("\n".join(errors))
    print(
        f"Editor OK: {QA_DOCX.name}, {QA_PDF.name}, "
        f"7 slides, {len(errors)} browser errors"
    )


if __name__ == "__main__":
    asyncio.run(main())
