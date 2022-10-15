from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_inpage_anchor_targets_exist(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    anchors = page.locator("a[href^='#']")
    for i in range(min(20, anchors.count())):
        href = anchors.nth(i).get_attribute("href") or ""
        target = href[1:]
        if not target:
            continue
        el = page.locator(f"#{target}")
        assert el.count() >= 0


