from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage
from utils.assets import collect_image_urls, collect_document_urls, head_statuses


@pytest.mark.smoke
def test_riga_images_are_available(context, page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    imgs = collect_image_urls(page, riga_base_url)[:50]
    statuses = head_statuses(context, imgs)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f"Broken images: {broken}"


def test_riga_documents_are_downloadable(context, page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    docs = collect_document_urls(page, riga_base_url)[:20]
    if not docs:
        return
    statuses = head_statuses(context, docs)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f"Broken documents: {broken}"


