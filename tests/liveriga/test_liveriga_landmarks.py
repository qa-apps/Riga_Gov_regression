from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.a11y
def test_liveriga_aria_landmarks_present(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    expect(page.get_by_role("banner")).to_be_visible(timeout=10000)
    expect(page.get_by_role("navigation")).to_be_visible(timeout=10000)
    expect(page.get_by_role("main")).to_be_visible(timeout=10000)
    expect(page.get_by_role("contentinfo")).to_be_visible(timeout=10000)


