from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage
from utils.crawl import collect_links, visit_urls
from utils.security import check_security_headers


@pytest.mark.smoke
def test_liveriga_footer_links(context, page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    footer = page.locator("footer")
    assert footer.locator("a[href]").count() > 0
    urls = collect_links(page, liveriga_base_url)[-40:]
    result = visit_urls(context, liveriga_base_url, urls, delay_ms=50)
    assert len(result.failed_urls) == 0, f"Broken footer links: {result.failed_urls}"


@pytest.mark.security
def test_liveriga_security_headers(context, liveriga_base_url) -> None:
    hdrs = check_security_headers(context, liveriga_base_url)
    baseline = {"x-content-type-options"}
    assert baseline.issubset({name for name, ok in hdrs if ok})


