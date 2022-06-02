from __future__ import annotations

import pytest

from utils.samples import sample_internal_pages
from utils.assets import collect_image_urls, head_statuses
from page_objects.riga.home import RigaHomePage


def test_riga_sample_pages_have_no_broken_images(context, page, riga_base_url) -> None:
    pages = sample_internal_pages(context, riga_base_url, max_pages=10)
    broken_total = []
    for url in pages:
        page.goto(url)
        imgs = collect_image_urls(page, riga_base_url)[:30]
        statuses = head_statuses(context, imgs)
        broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
        broken_total.extend(broken)
    assert len(broken_total) == 0, f"Broken images across sample: {broken_total[:10]}"


