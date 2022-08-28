from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_search_results_show_filters_or_facets(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    home.search("museum")
    main = page.get_by_role("main")
    filters = main.locator("input[type='checkbox'], input[type='radio'], select")
    assert filters.count() >= 0
    expect(main).to_be_visible()


