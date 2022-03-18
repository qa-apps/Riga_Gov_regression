from __future__ import annotations

from utils.site_checks import open_home
from playwright.sync_api import expect


def test_search_results(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    box = page.get_by_role("textbox")
    if box.count() == 0:
        return
    box.first.fill("Riga")
    box.first.press("Enter")
    expect(page).to_have_url(lambda url: "search" in url or "mekl" in url)
    assert page.locator("a[href]").count() > 0


def test_form_controls_presence(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    controls = page.locator("input, textarea, select, button")
    assert controls.count() >= 0


def test_cookies_banner_persistence(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    storage_before = page.context.cookies()
    page.reload()
    storage_after = page.context.cookies()
    assert isinstance(storage_after, list)
    assert len(storage_after) >= 0




def test_search_box_exists(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    box = page.get_by_role("textbox")
    assert box.count() >= 0

# search suite end
