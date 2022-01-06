from __future__ import annotations

import os
import time
from typing import List

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage
from utils.crawl import collect_links, visit_urls


@pytest.mark.smoke
def test_riga_homepage_primary_links(context, page, base_url) -> None:
    # Override base_url for riga if env provided
    riga_url = os.getenv("RIGA_BASE_URL", "https://www.riga.lv")
    home = RigaHomePage(page, riga_url)
    home.open()
    home.open_menu()

    # Collect and visit a bounded set of unique links from the homepage
    urls: List[str] = collect_links(page, riga_url)[:50]
    result = visit_urls(context, riga_url, urls, delay_ms=50)

    # All checked URLs should be ok (status >= 200 and < 400)
    assert len(result.failed_urls) == 0, f"Broken links: {result.failed_urls}"

    # Basic content check after returning to home
    page.goto(riga_url)
    expect(page.get_by_role("heading")).to_be_visible()


