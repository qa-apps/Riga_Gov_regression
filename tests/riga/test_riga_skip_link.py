from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.a11y
def test_riga_skip_to_content_link(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    skip = page.get_by_role("link", name=lambda s: "Skip" in s or "Uz saturu" in s or "Pāriet uz saturu" in s)
    expect(skip.first).to_be_visible()


