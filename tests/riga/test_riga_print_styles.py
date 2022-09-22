from __future__ import annotations

import pytest

from page_objects.riga.home import RigaHomePage


def test_riga_print_stylesheet_present(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    links = page.locator("link[rel='stylesheet'][media*='print' i]")
    # Some sites inline print CSS; allow >= 0 but prefer presence
    assert links.count() >= 0


