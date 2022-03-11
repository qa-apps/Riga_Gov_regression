from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage
from utils.assets import collect_image_urls, collect_document_urls, head_statuses


@pytest.mark.smoke
def test_liveriga_images_are_available(context, page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    imgs = collect_image_urls(page, liveriga_base_url)[:50]
    statuses = head_statuses(context, imgs)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f\"Broken images: {broken}\"


def test_liveriga_documents_are_downloadable(context, page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    docs = collect_document_urls(page, liveriga_base_url)[:20]
    if not docs:
        return
    statuses = head_statuses(context, docs)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f\"Broken documents: {broken}\"


