from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.smoke
def test_liveriga_mobile_menu_can_open(browser, liveriga_base_url) -> None:
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    home.open_menu()
    expect(page.get_by_role("navigation").get_by_role("link").first).to_be_visible()
    context.close()


