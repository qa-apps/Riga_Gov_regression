from __future__ import annotations

from utils.site_checks import check_security_headers
from playwright.sync_api import expect


def _assert_headers(headers: dict) -> None:
    assert headers.get("x-content-type-options") in ("nosniff", "NOSNIFF", None)
    # Others may vary by platform; only assert presence when served
    for key in (
        "content-security-policy",
        "strict-transport-security",
        "referrer-policy",
        "permissions-policy",
    ):
        assert key in headers


def test_riga_security_headers(context, riga_base_url) -> None:
    headers = check_security_headers(context, riga_base_url)
    _assert_headers(headers)


def test_liveriga_security_headers(context, liveriga_base_url) -> None:
    headers = check_security_headers(context, liveriga_base_url)
    _assert_headers(headers)


def test_external_link_policy(page, riga_base_url) -> None:
    page.goto(riga_base_url, wait_until="domcontentloaded")
    external = page.locator("a[target='_blank']").first
    if external.count() == 0:
        return
    rel = external.get_attribute("rel") or ""
    assert "noopener" in rel or "noreferrer" in rel


def test_https_redirects(context, riga_base_url) -> None:
    http_url = riga_base_url.replace("https://", "http://")
    resp = context.request.get(http_url, max_redirects=0)
    assert resp.status in (301, 302, 307, 308)


