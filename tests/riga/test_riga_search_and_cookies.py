from __future__ import annotations

import os
import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.smoke
def test_riga_search_results(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    home.search("budžets")
    expect(page.get_by_role("main")).to_be_visible()
    # Ensure there are some results markers
    expect(page.locator("a[href]")).to_have_count(lambda c: c > 0)


def test_riga_cookie_banner_persistence(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    # Try to accept cookies via common selectors
    btn = page.get_by_role("button", name=lambda s: "Sapratu" in s or "Piekrītu" in s or "Accept" in s)
    if btn.count() == 0:
        btn = page.locator("button:has-text('Sapratu'), button:has-text('Piekrītu'), button:has-text('Accept')")
    if btn.count() > 0:
        btn.first.click()
        page.reload()
        # Banner should not reappear
        assert btn.count() == 0


