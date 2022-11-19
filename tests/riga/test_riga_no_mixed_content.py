from __future__ import annotations

import pytest

from page_objects.riga.home import RigaHomePage


def test_riga_homepage_has_no_mixed_content(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    # Look for http:// references in link/script/img tags
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
    assert len(http_refs) == 0, f"Mixed content references: {http_refs.slice(0,5)}"


