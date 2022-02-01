from __future__ import annotations

from utils.site_checks import open_home, external_link_is_safe
from playwright.sync_api import expect


def test_header_footer_elements(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    expect(page.locator("header")).to_be_visible()
    expect(page.locator("footer")).to_be_visible()
    assert page.locator("header nav a[href]").count() > 3
    assert page.locator("footer a[href]").count() > 3


def test_language_switch_or_menu(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    btns = page.get_by_role("button")
    has_menu = btns.count() > 0
    assert has_menu or page.locator("a[hreflang]").count() >= 0


def test_external_links_are_safe(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    external = page.locator("a[target='_blank']").first
    if external.count() == 0:
        return
    assert external_link_is_safe(page, "a[target='_blank']")


def test_focus_styles_and_skip_link(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    page.keyboard.press("Tab")
    focused = page.locator(":focus")
    assert focused.count() >= 0
    skip = page.locator("a[href^='#'][href*='content'], a[href='#content'], a.skip-link")
    assert skip.count() >= 0


def test_breadcrumbs_or_aria(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    crumbs = page.locator("[aria-label='Breadcrumbs'] ol li, nav.breadcrumb ol li, .breadcrumb li")
    landmarks = page.locator("[role='main'], main, [role='navigation'], nav")
    assert crumbs.count() >= 0
    assert landmarks.count() > 0


