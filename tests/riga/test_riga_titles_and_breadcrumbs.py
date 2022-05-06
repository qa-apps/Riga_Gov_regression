from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage
from utils.crawl import collect_links


@pytest.mark.smoke
def test_riga_homepage_title_not_empty(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    title = page.title()
    assert isinstance(title, str) and len(title.strip()) > 0


def test_riga_sample_content_has_breadcrumbs(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    urls = collect_links(page, riga_base_url)[:5]
    for url in urls:
        page.goto(url)
        crumbs = page.locator(\"nav[aria-label*='crumb'], .breadcrumb, .breadcrumbs\")
        # Not all pages have breadcrumbs; require at least one in sample set
        if crumbs.count() > 0:
            expect(crumbs).to_be_visible()
            return
    # If loop completes without return, fail once
    assert False, \"No breadcrumbs found in sample pages\"


