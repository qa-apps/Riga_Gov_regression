from __future__ import annotations

from playwright.sync_api import expect
from page_objects.home_page import HomePage


def test_homepage_h1_contains_example(page, base_url) -> None:
    home = HomePage(page, base_url)
    home.open()
    expect(page.locator("h1")).to_have_text("Example Domain")


