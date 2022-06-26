from __future__ import annotations

import pytest

from utils.samples import sample_internal_pages
from utils.security import get_headers, SECURITY_HEADERS


@pytest.mark.security
def test_riga_sample_pages_have_key_security_headers(context, riga_base_url) -> None:
    pages = sample_internal_pages(context, riga_base_url, max_pages=8)
    baseline = {"x-content-type-options"}
    present_all = True
    for url in pages:
        headers = get_headers(context, url)
        if not baseline.issubset(set(k for k in headers.keys())):
            present_all = False
            break
    assert present_all, "Some sample pages are missing baseline headers"


