from __future__ import annotations

import os
import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


VIEWPORTS = [
    (1920, 1080),
    (1366, 768),
    (1024, 768),
    (414, 896),  # iPhone XR
    (390, 844),  # iPhone 12/13
]


@pytest.mark.parametrize("width,height", VIEWPORTS)
def test_riga_responsive_layout(browser, riga_base_url, width, height) -> None:
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    home = RigaHomePage(page, riga_base_url)
    home.open()
    # Try to open mobile menu if present on small widths
    if width < 768:
        home.open_menu()
    expect(page.get_by_role("main")).to_be_visible()
    context.close()


