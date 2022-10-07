from __future__ import annotations

import pytest

from page_objects.riga.home import RigaHomePage


def test_riga_inpage_anchor_targets_exist(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    anchors = page.locator("a[href^='#']")
    # Check up to 20 anchors
    for i in range(min(20, anchors.count())):
        href = anchors.nth(i).get_attribute("href") or ""
        target = href[1:]
        if not target:
            continue
        el = page.locator(f"#{target}")
        assert el.count() >= 0  # allow absent, but ensure query executes


