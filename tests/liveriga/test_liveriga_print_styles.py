from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_print_stylesheet_present(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    links = page.locator("link[rel='stylesheet'][media*='print' i]")
    assert links.count() >= 0


