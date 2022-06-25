from __future__ import annotations

import pytest


@pytest.mark.security
def test_riga_robots_txt_exists(context, riga_base_url) -> None:
    url = riga_base_url.rstrip("/") + "/robots.txt"
    resp = context.request.get(url, timeout=15000)
    assert resp.ok, f"robots.txt status {resp.status}"
    text = resp.text()
    assert "User-agent" in text or "Sitemap" in text


@pytest.mark.security
def test_liveriga_robots_txt_exists(context, liveriga_base_url) -> None:
    url = liveriga_base_url.rstrip("/") + "/robots.txt"
    resp = context.request.get(url, timeout=15000)
    assert resp.ok, f"robots.txt status {resp.status}"
    text = resp.text()
    assert "User-agent" in text or "Sitemap" in text


