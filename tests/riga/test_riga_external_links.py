from __future__ import annotations

import pytest
from urllib.parse import urlparse

from page_objects.riga.home import RigaHomePage


def is_external(url: str, base: str) -> bool:
    return urlparse(url).netloc and urlparse(url).netloc != urlparse(base).netloc


@pytest.mark.security
def test_riga_external_links_have_noopener(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    anchors = page.query_selector_all("a[href]")
    external = []
    for a in anchors:
        href = a.get_attribute("href") or ""
        if not href:
            continue
        full = page.evaluate("(u, b) => new URL(u, b).toString()", href, riga_base_url)
        if is_external(full, riga_base_url):
            rel = (a.get_attribute("rel") or "").lower()
            target = (a.get_attribute("target") or "").lower()
            if target == "_blank":
                external.append((full, rel))
    # If there are external _blank links, they should include noopener
    for url, rel in external[:50]:
        assert "noopener" in rel or "noreferrer" in rel, f"Missing noopener for {url}"


