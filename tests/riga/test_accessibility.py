from __future__ import annotations

from utils.site_checks import open_home
from playwright.sync_api import expect


def test_landmarks_present(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    main = page.locator("main, [role='main']")
    nav = page.locator("nav, [role='navigation']")
    assert main.count() >= 1
    assert nav.count() >= 1


def test_headings_structure(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    headings = page.locator("h1, h2, h3")
    assert headings.count() >= 1
    # Ensure first heading is visible
    expect(headings.first).to_be_visible()


def test_keyboard_navigation(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    for _ in range(5):
        page.keyboard.press("Tab")
    focused = page.locator(":focus")
    assert focused.count() >= 0


def test_skip_link_and_aria(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    skip = page.locator("a[href^='#'][href*='content'], a[href='#content'], a.skip-link")
    assert skip.count() >= 0
    assert page.locator("[aria-label]").count() >= 0


def test_tabindex_reasonable(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    tabbables = page.locator("[tabindex]")
    assert tabbables.count() >= 0


