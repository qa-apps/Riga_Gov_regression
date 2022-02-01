from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.smoke
def test_liveriga_search(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    home.search("museum")
    expect(page.get_by_role("main")).to_be_visible()


@pytest.mark.parametrize(\"width,height\", [(1280, 800), (768, 1024), (414, 896)])
def test_liveriga_responsive(browser, liveriga_base_url, width, height) -> None:
    context = browser.new_context(viewport={\"width\": width, \"height\": height})
    page = context.new_page()
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    if width < 768:
        home.open_menu()
    expect(page.get_by_role(\"main\")).to_be_visible()
    context.close()


