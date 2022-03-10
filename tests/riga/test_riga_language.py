from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.smoke
def test_riga_language_switch_presence(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    # Look for a language switcher link/button commonly used
    lang = page.get_by_role("link", name=lambda s: "EN" in s or "LV" in s or "RU" in s)
    if lang.count() == 0:
        lang = page.get_by_role("button", name=lambda s: "EN" in s or "LV" in s or "RU" in s)
    expect(lang.first).to_be_visible()


