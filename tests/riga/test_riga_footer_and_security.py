from __future__ import annotations

import os
import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage
from utils.crawl import collect_links, visit_urls
from utils.security import check_security_headers


@pytest.mark.smoke
def test_riga_footer_links(context, page, base_url) -> None:
    riga_url = os.getenv("RIGA_BASE_URL", "https://www.riga.lv")
    home = RigaHomePage(page, riga_url)
    home.open()
    footer_count = home.footer_links()
    assert footer_count > 0

    urls = collect_links(page, riga_url)[-40:]
    result = visit_urls(context, riga_url, urls, delay_ms=50)
    assert len(result.failed_urls) == 0, f"Broken footer links: {result.failed_urls}"


@pytest.mark.security
def test_riga_security_headers(context, page, base_url) -> None:
    riga_url = os.getenv("RIGA_BASE_URL", "https://www.riga.lv")
    # Home page headers
    hdrs = check_security_headers(context, riga_url)
    missing = [name for name, ok in hdrs if not ok]
    # Not all public sites expose all headers; require a baseline subset
    baseline = {"strict-transport-security", "x-content-type-options"}
    assert baseline.issubset({name for name, ok in hdrs if ok}), f"Missing baseline headers: {missing}"


