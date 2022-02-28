from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.smoke
def test_riga_header_footer_and_breadcrumb(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    # Header and footer presence
    expect(page.get_by_role("navigation")).to_be_visible()
    expect(page.locator("footer")).to_be_visible()
    # Navigate to a content page by clicking the first visible article/link
    link = page.locator("main a[href]").first
    if link.count() > 0:
        href = link.get_attribute("href")
        link.click()
        expect(page).to_have_url(lambda u: u != riga_base_url and isinstance(u, str))
        # Breadcrumbs often present
        crumbs = page.locator("nav[aria-label*='crumb'], .breadcrumb, .breadcrumbs")
        expect(crumbs).to_be_visible()


