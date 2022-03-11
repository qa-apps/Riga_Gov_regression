from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.smoke
def test_liveriga_language_switch_presence(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    lang = page.get_by_role("link", name=lambda s: "EN" in s or "LV" in s or "RU" in s)
    if lang.count() == 0:
        lang = page.get_by_role("button", name=lambda s: "EN" in s or "LV" in s or "RU" in s)
    expect(lang.first).to_be_visible()


