from __future__ import annotations

import os

import pytest


def _http_url(https_url: str) -> str:
    return https_url.replace("https://", "http://", 1)


@pytest.mark.security
def test_riga_http_redirects_to_https(context, riga_base_url) -> None:
    http = _http_url(riga_base_url)
    resp = context.request.get(http, max_redirects=0)
    # Some servers return 301/302/308 permanent redirects
    assert 300 <= resp.status < 400
    assert resp.headers.get("location", "").startswith("https://")


@pytest.mark.security
def test_liveriga_http_redirects_to_https(context, liveriga_base_url) -> None:
    http = _http_url(liveriga_base_url)
    resp = context.request.get(http, max_redirects=0)
    assert 300 <= resp.status < 400
    assert resp.headers.get("location", "").startswith("https://")


