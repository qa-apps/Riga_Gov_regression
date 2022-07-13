from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.smoke
def test_riga_mobile_menu_can_open(browser, riga_base_url) -> None:
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    home = RigaHomePage(page, riga_base_url)
    home.open()
    home.open_menu()
    # Verify that menu links are visible
    expect(page.get_by_role("navigation").get_by_role("link").first).to_be_visible()
    context.close()


