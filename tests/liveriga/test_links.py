from __future__ import annotations

from utils.crawler import crawl_site
from utils.site_checks import open_home


def test_liveriga_crawl_links(page, context, liveriga_base_url, crawl_limit) -> None:
    open_home(page, liveriga_base_url)
    result = crawl_site(context, liveriga_base_url, max_pages=crawl_limit)
    assert result.visited, "no pages visited"
    assert not any("bad status" in r[1] for r in result.failures)


def test_liveriga_nav_is_present(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    assert page.locator("nav a[href]").count() > 3


