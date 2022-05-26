from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage
from utils.crawl import collect_links


def _first_form_selector():
    return "main form, form[action]"


@pytest.mark.smoke
def test_riga_first_form_has_required_fields(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    links = collect_links(page, riga_base_url)[:10]
    for url in links:
        page.goto(url)
        form = page.locator(_first_form_selector()).first
        if form.count() == 0:
            continue
        # Text fields exist
        inputs = form.locator("input[type='text'], input[type='email'], textarea")
        if inputs.count() == 0:
            continue
        expect(inputs.first).to_be_visible()
        return
    assert False, "No form with text inputs found among sampled pages"


