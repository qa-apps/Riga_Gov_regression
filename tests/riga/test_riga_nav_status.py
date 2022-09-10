from __future__ import annotations

import pytest

from page_objects.riga.home import RigaHomePage
from utils.crawl import collect_links, check_urls


def test_riga_header_nav_links_are_reachable(context, page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    home.open_menu()
    nav_links = page.get_by_role("navigation").locator("a[href]")
    hrefs = []
    for i in range(min(30, nav_links.count())):
        href = nav_links.nth(i).get_attribute("href")
        if href:
            hrefs.append(href)
    urls = [page.evaluate("(u, b) => new URL(u, b).toString()", h, riga_base_url) for h in hrefs]
    statuses = check_urls(context, urls)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f"Broken header links: {broken}"


