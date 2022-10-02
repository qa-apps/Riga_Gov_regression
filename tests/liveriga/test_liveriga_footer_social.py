from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage
from utils.crawl import check_urls


def test_liveriga_footer_social_links_are_reachable(context, page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    footer = page.locator("footer")
    links = footer.locator("a[href*='facebook'], a[href*='twitter'], a[href*='instagram'], a[href*='youtube'], a[href*='flickr']")
    hrefs = []
    for i in range(min(10, links.count())):
        href = links.nth(i).get_attribute("href")
        if href:
            hrefs.append(href)
    if not hrefs:
        pytest.skip("No social links found in footer")
    statuses = check_urls(context, hrefs)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f"Broken social links: {broken}"


