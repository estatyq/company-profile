"""Browser-level test for /admin, multilingual editing and first-visit routing."""

from __future__ import annotations

import asyncio
import json
import pathlib
import shutil
import sys
import tempfile
import threading

from playwright.async_api import async_playwright
from werkzeug.serving import make_server


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app as application  # noqa: E402


async def run_browser(base_url: str, preview: pathlib.Path) -> None:
    errors = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(channel="chrome")
        context = await browser.new_context(
            viewport={"width": 1440, "height": 1000},
            accept_downloads=True,
        )
        page = await context.new_page()
        page.on(
            "console",
            lambda message: errors.append(f"console:{message.type}:{message.text}")
            if message.type == "error"
            else None,
        )
        page.on("pageerror", lambda error: errors.append(f"pageerror:{error}"))
        await page.goto(f"{base_url}/admin", wait_until="networkidle")
        assert await page.get_by_text("Создайте пароль администратора").is_visible()
        await page.locator('input[name="password"]').fill("StrongBrowserPass!2026")
        await page.locator('input[name="confirmation"]').fill("StrongBrowserPass!2026")
        await page.get_by_role("button", name="Создать пароль и войти").click()
        await page.wait_for_load_state("networkidle")
        assert await page.get_by_text("Управление профилем").is_visible()
        assert await page.locator("[data-language]").count() == 5

        await page.locator("#brand-field").fill("Global Studio")
        await page.locator("#contact-email").fill("hello@global.studio")
        await page.locator("#contact-whatsapp").fill("+49 151 23456789")
        await page.locator("#brand-logo-file").set_input_files(
            ROOT / "assets" / "web" / "forma_doc.jpg"
        )
        await page.wait_for_function(
            """() => document.querySelector(
                '#brand-logo-preview img'
            )?.src.includes('/uploads/')"""
        )
        await page.locator("#add-project").click()
        project = page.locator(".admin-project").last
        await project.locator('[data-project-field="name"]').fill("Global Project")
        await project.locator('[data-project-field="url"]').fill(
            "https://example.com/global"
        )
        await project.locator('[data-project-field="coverSub"]').fill(
            "Digital platform"
        )
        await project.locator('[data-project-field="features"]').fill(
            "Client portal\nAutomated workflow"
        )
        await project.locator('[data-upload-image]').set_input_files(
            ROOT / "assets" / "web" / "rieltix_site.jpg"
        )
        await page.wait_for_function(
            """() => document.querySelector(
                '.admin-project:last-of-type .project-thumb img'
            )?.src.includes('/uploads/')"""
        )
        await page.locator('[data-language="es"]').click()
        assert await page.get_by_text("Вы редактируете версию: Español.").is_visible()
        await page.locator('[data-text-key="p6_title"]').fill("Cómo trabajamos juntos")
        await page.screenshot(path=str(preview / "admin_dashboard.png"), full_page=True)
        await page.locator("#save-content").click()
        await page.get_by_text("Изменения опубликованы").wait_for()

        public_context = await browser.new_context(viewport={"width": 1440, "height": 900})
        public_page = await public_context.new_page()
        await public_page.goto(f"{base_url}/", wait_until="networkidle")
        gate = public_page.locator("#language-gate")
        assert await gate.is_visible()
        assert await gate.locator("[data-language-choice]").count() == 5
        await public_page.screenshot(
            path=str(preview / "language_selector.png"),
            full_page=False,
        )
        await gate.locator('[data-language-choice="es"]').click()
        await public_page.wait_for_url("**/es.html")
        await public_page.wait_for_load_state("networkidle")
        assert (
            await public_page.locator(".mark span").first.text_content()
        ).strip() == "Global Studio"
        assert await public_page.locator(".mark .brand-logo").count() >= 1
        assert (
            await public_page.locator(".p6 .title h2").first.text_content()
        ).strip() == "Cómo trabajamos juntos"
        assert await public_page.get_by_text("Global Project", exact=True).count() >= 1
        await public_page.screenshot(
            path=str(preview / "public_spanish_after_admin.png"),
            full_page=False,
        )
        await public_context.close()
        await context.close()
        await browser.close()
    if errors:
        raise RuntimeError("\n".join(errors))


async def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        temp = pathlib.Path(temporary)
        site = temp / "site"
        shutil.copytree(ROOT / "site", site)
        data = temp / "data"
        data.mkdir()
        application.DATA_DIR = data
        application.SITE_DIR = site
        application.UPLOAD_DIR = site / "assets" / "web" / "uploads"
        application.PROFILE_STORE = data / "profile.json"
        application.ADMIN_CREDENTIALS = data / "admin.json"
        application.SESSION_SECRET_FILE = data / ".session_secret"
        application.BACKUP_DIR = data / "backups"
        application.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        application.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        application.LOGIN_FAILURES.clear()
        application.app.config.update(
            TESTING=True,
            SECRET_KEY="browser-test-secret",
        )

        server = make_server("127.0.0.1", 0, application.app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        preview = ROOT / "output" / "preview"
        preview.mkdir(parents=True, exist_ok=True)
        try:
            await run_browser(f"http://127.0.0.1:{server.server_port}", preview)
        finally:
            server.shutdown()
            thread.join(timeout=3)

    print("Admin browser OK: setup, 5 languages, upload, save, first-visit routing")


if __name__ == "__main__":
    asyncio.run(main())
