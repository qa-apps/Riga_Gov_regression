from __future__ import annotations

import pytest
from urllib.parse import urlparse

from page_objects.liveriga.home import LiveRigaHomePage


def is_external(url: str, base: str) -> bool:
    return urlparse(url).netloc and urlparse(url).netloc != urlparse(base).netloc


@pytest.mark.security
def test_liveriga_external_links_have_noopener(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    anchors = page.query_selector_all("a[href]")
    external = []
    for a in anchors:
        href = a.get_attribute("href") or ""
        if not href:
            continue
        full = page.evaluate("(u, b) => new URL(u, b).toString()", href, liveriga_base_url)
        if is_external(full, liveriga_base_url):
            rel = (a.get_attribute("rel") or "").lower()
            target = (a.get_attribute("target") or "").lower()
            if target == "_blank":
                external.append((full, rel))
    for url, rel in external[:50]:
        assert "noopener" in rel or "noreferrer" in rel, f"Missing noopener for {url}"


