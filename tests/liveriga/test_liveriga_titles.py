from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.smoke
def test_liveriga_homepage_title_and_heading(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    title = page.title()
    assert isinstance(title, str) and len(title.strip()) > 0
    expect(page.get_by_role("heading")).to_be_visible()


