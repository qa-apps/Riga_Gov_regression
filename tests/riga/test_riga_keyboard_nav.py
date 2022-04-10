from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.a11y
def test_riga_primary_menu_keyboard_navigation(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    # Focus first focusable element in navigation and move through items
    nav = page.get_by_role("navigation")
    first_link = nav.get_by_role("link").first
    first_link.focus()
    expect(first_link).to_be_focused()
    for _ in range(5):
        page.keyboard.press("Tab")
    # After several tabs, focus should remain within page
    expect(page.locator(":focus")).to_be_visible()


