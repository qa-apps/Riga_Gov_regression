from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


def _accept_or_open_settings(page):
    btn = page.get_by_role("button", name=lambda s: "Sapratu" in s or "Piekrītu" in s or "Accept" in s)
    if btn.count() == 0:
        btn = page.locator("button:has-text('Sapratu'), button:has-text('Piekrītu'), button:has-text('Accept')")
    if btn.count() > 0:
        btn.first.click()
        return True
    # Settings button
    settings = page.get_by_role("button", name=lambda s: "Sīkdatņu" in s or "Cookie" in s or "Preferences" in s)
    if settings.count() > 0:
        settings.first.click()
        return True
    return False


def test_riga_cookie_preferences_flow(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    if not _accept_or_open_settings(page):
        return
    page.reload()
    # Cookie banner should be dismissed or preferences remembered
    banner = page.get_by_role("dialog", name=lambda s: "Sīkdatņu" in s or "Cookie" in s)
    assert banner.count() == 0


