from __future__ import annotations

import pytest
from playwright.sync_api import expect

from utils.samples import sample_internal_pages
from page_objects.riga.home import RigaHomePage


def test_riga_sample_pages_expose_breadcrumbs_semantics(page, riga_base_url, context) -> None:
    pages = sample_internal_pages(context, riga_base_url, max_pages=8)
    has_crumbs = False
    for url in pages:
        page.goto(url)
        crumbs = page.locator(\"nav[aria-label*='crumb' i], .breadcrumb, .breadcrumbs\")
        if crumbs.count() > 0:
            has_crumbs = True
            expect(crumbs).to_be_visible()
            break
    assert has_crumbs, \"No breadcrumbs semantics found in sampled pages\"


