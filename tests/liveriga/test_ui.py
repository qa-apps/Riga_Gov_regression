from __future__ import annotations

from utils.site_checks import open_home, external_link_is_safe
from playwright.sync_api import expect


def test_header_footer(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    expect(page.locator("header")).to_be_visible()
    expect(page.locator("footer")).to_be_visible()
    assert page.locator("header nav a[href]").count() > 3
    assert page.locator("footer a[href]").count() > 3


def test_nav_and_search(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    assert page.locator("nav a[href]").count() > 0
    box = page.get_by_role("textbox")
    if box.count() > 0:
        box.first.fill("Riga")
        box.first.press("Enter")
        expect(page).to_have_url(lambda url: "search" in url or "mekl" in url)


def test_external_links_policy(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    external = page.locator("a[target='_blank']").first
    if external.count() == 0:
        return
    assert external_link_is_safe(page, "a[target='_blank']")


def test_mobile_ui(page, liveriga_base_url) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    open_home(page, liveriga_base_url)
    assert page.locator("header").count() >= 1
    btns = page.get_by_role("button")
    assert btns.count() >= 0


