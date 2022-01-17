from __future__ import annotations

from typing import Dict, List, Tuple
from playwright.sync_api import BrowserContext


SECURITY_HEADERS = [
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
]


def get_headers(context: BrowserContext, url: str) -> Dict[str, str]:
    """Return response headers map for a GET request to url."""
    resp = context.request.get(url, timeout=20000)
    headers = {k.lower(): v for k, v in resp.headers.items()}
    return headers


def check_security_headers(context: BrowserContext, url: str) -> List[Tuple[str, bool]]:
    """Return list of (header, present) for required security headers."""
    headers = get_headers(context, url)
    results: List[Tuple[str, bool]] = []
    for name in SECURITY_HEADERS:
        results.append((name, name in headers))
    return results


