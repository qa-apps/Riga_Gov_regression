from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.a11y
def test_liveriga_primary_menu_keyboard_navigation(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    nav = page.get_by_role("navigation")
    first_link = nav.get_by_role("link").first
    first_link.focus()
    expect(first_link).to_be_focused()
    for _ in range(5):
        page.keyboard.press("Tab")
    expect(page.locator(":focus")).to_be_visible()


