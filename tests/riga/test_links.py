from __future__ import annotations

from utils.crawler import crawl_site
from utils.site_checks import open_home


def test_riga_crawl_links(page, context, riga_base_url, crawl_limit) -> None:
    open_home(page, riga_base_url)
    result = crawl_site(context, riga_base_url, max_pages=crawl_limit)
    assert result.visited, "no pages visited"
    assert not any("bad status" in r[1] for r in result.failures)


def test_riga_nav_is_present(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    nav = page.locator("nav")
    assert nav.count() > 0
    assert page.locator("nav a[href]").count() > 3


