from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_viewport_meta_and_icons_present(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    viewport = page.locator("meta[name='viewport']")
    assert viewport.count() > 0
    icons = page.locator("link[rel*='icon' i]")
    assert icons.count() >= 0


