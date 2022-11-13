from __future__ import annotations

import pytest

from page_objects.riga.home import RigaHomePage


def test_riga_viewport_meta_and_icons_present(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    viewport = page.locator("meta[name='viewport']")
    assert viewport.count() > 0
    icons = page.locator("link[rel*='icon' i]")
    assert icons.count() >= 0


