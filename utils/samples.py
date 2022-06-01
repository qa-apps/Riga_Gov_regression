from __future__ import annotations

from typing import List
from urllib.parse import urlparse

from playwright.sync_api import BrowserContext

from .deepcrawl import deep_crawl


def sample_internal_pages(context: BrowserContext, base_url: str, max_pages: int = 20) -> List[str]:
    """Return a small sample of internal pages using deep crawl starting at base_url."""
    result = deep_crawl(context, base_url, max_pages=max_pages, max_depth=2)
    pages = [u for u in result.visited if urlparse(u).netloc == urlparse(base_url).netloc]
    # Ensure base_url is included first
    unique = []
    seen = set()
    for u in [base_url] + pages:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique[:max_pages]


