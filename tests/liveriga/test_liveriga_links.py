from __future__ import annotations

import os
import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage
from utils.crawl import collect_links, visit_urls


@pytest.mark.smoke
def test_liveriga_homepage_links(context, page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    home.open_menu()
    urls = collect_links(page, liveriga_base_url)[:50]
    result = visit_urls(context, liveriga_base_url, urls, delay_ms=50)
    assert len(result.failed_urls) == 0, f"Broken links: {result.failed_urls}"
    page.goto(liveriga_base_url)
    expect(page.get_by_role("heading")).to_be_visible()


