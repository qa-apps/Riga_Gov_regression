from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.a11y
def test_riga_aria_landmarks_present(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    expect(page.get_by_role("banner")).to_be_visible(timeout=10000)
    expect(page.get_by_role("navigation")).to_be_visible(timeout=10000)
    expect(page.get_by_role("main")).to_be_visible(timeout=10000)
    expect(page.get_by_role("contentinfo")).to_be_visible(timeout=10000)


