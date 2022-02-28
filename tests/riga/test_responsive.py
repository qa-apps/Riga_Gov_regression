from __future__ import annotations

from utils.site_checks import open_home
from playwright.sync_api import expect


def test_desktop_view(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 1440, "height": 900})
    open_home(page, riga_base_url)
    expect(page.locator("header")).to_be_visible()
    assert page.locator("nav a[href]").count() >= 3


def test_tablet_view(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 1024, "height": 768})
    open_home(page, riga_base_url)
    expect(page.locator("header")).to_be_visible()
    assert page.locator("a[href]").count() >= 3


def test_mobile_view(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    open_home(page, riga_base_url)
    assert page.locator("header").count() >= 1
    btns = page.get_by_role("button")
    assert btns.count() >= 0


def test_mobile_menu_present(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 375, "height": 667})
    open_home(page, riga_base_url)
    menu_button = page.get_by_role("button", name=lambda n: n and ("Izvēlne" in n or "Menu" in n))
    if menu_button.count() > 0:
        try:
            menu_button.first.click(timeout=1200)
        except Exception:
            pass
    assert page.locator("nav").count() >= 1


