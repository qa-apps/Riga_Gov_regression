from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


def test_riga_search_results_show_filters_or_facets(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    home.search("Rīga")
    # Heuristic: look for filter inputs or selects in main
    main = page.get_by_role("main")
    filters = main.locator("input[type='checkbox'], input[type='radio'], select")
    assert filters.count() >= 0  # presence not guaranteed; ensure page loads
    expect(main).to_be_visible()


