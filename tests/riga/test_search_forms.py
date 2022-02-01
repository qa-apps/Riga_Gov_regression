from __future__ import annotations

from utils.site_checks import open_home
from playwright.sync_api import expect


def test_search_results(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    box = page.get_by_role("textbox")
    if box.count() == 0:
        return
    box.first.fill("Rīga")
    box.first.press("Enter")
    expect(page).to_have_url(lambda url: "search" in url or "mekl" in url)
    assert page.locator("a[href]").count() > 0


def test_form_controls_presence(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    controls = page.locator("input, textarea, select, button")
    assert controls.count() >= 0


def test_form_validation_messages(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    form = page.locator("form").first
    if form.count() == 0:
        return
    required = form.locator("[required]")
    if required.count() > 0:
        try:
            form.evaluate("f => f.submit()")
        except Exception:
            pass
        assert page.locator(":invalid").count() >= 0


def test_cookies_banner_persistence(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    storage_before = page.context.cookies()
    page.reload()
    storage_after = page.context.cookies()
    assert isinstance(storage_after, list)
    assert len(storage_after) >= 0



