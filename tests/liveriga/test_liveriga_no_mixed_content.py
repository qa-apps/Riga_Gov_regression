from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_homepage_has_no_mixed_content(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    http_refs = page.evaluate(
        """() => {
            const sel = ['img[src]', 'script[src]', 'link[href]'];
            const urls = [];
            sel.forEach(s => document.querySelectorAll(s).forEach(n => {
                const u = n.getAttribute('src') || n.getAttribute('href') || '';
                if (u.startsWith('http://')) urls.push(u);
            }));
            return urls;
        }"""
    )
    assert len(http_refs) == 0, `Mixed content references: ${http_refs.slice(0,5)}`


