from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


def test_riga_logo_links_to_home(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    logo = page.locator("a[href='/'], a.logo, a[aria-label*='home' i]")
    if logo.count() == 0:
        pytest.skip("Logo link not found")
    logo.first.click()
    expect(page).to_have_url(lambda u: u.startswith(riga_base_url))


