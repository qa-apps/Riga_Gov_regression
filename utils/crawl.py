from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple
from urllib.parse import urljoin, urlparse

from playwright.sync_api import BrowserContext, Page, expect


@dataclass
class CrawlResult:
    visited_urls: List[str]
    failed_urls: List[Tuple[str, int]]


def _is_in_domain(url: str, base_url: str) -> bool:
    base_host = urlparse(base_url).netloc
    url_host = urlparse(url).netloc
    return base_host == url_host or url_host == ""


def _normalize_url(href: str, base_url: str) -> str:
    if not href:
        return ""
    return urljoin(base_url, href)


def collect_links(page: Page, base_url: str, unique: bool = True) -> List[str]:
    """Collect visible anchor hrefs on the current page filtered to base domain."""
    hrefs = page.eval_on_selector_all(
        "a[href]",
        "(nodes) => nodes.map(n => ({href: n.getAttribute('href'), hidden: n.offsetParent === null }))",
    )
    urls: List[str] = []
    seen: Set[str] = set()
    for item in hrefs:
        href = _normalize_url(item.get("href") or "", base_url)
        if not href or not _is_in_domain(href, base_url):
            continue
        if unique:
            if href in seen:
                continue
            seen.add(href)
        urls.append(href)
    return urls


def check_urls(context: BrowserContext, urls: Iterable[str], delay_ms: int = 0) -> List[Tuple[str, int]]:
    """Return list of (url, status) by issuing requests using context.request."""
    results: List[Tuple[str, int]] = []
    for url in urls:
        if delay_ms:
            time.sleep(delay_ms / 1000.0)
        try:
            resp = context.request.get(url, timeout=20000)
            status = resp.status
        except Exception:
            status = 0
        results.append((url, status))
    return results


def visit_urls(context: BrowserContext, base_url: str, urls: Iterable[str], delay_ms: int = 50) -> CrawlResult:
    """Open each url in a fresh page to simulate navigation and basic rendering checks."""
    visited: List[str] = []
    failed: List[Tuple[str, int]] = []
    for url, status in check_urls(context, urls, delay_ms=delay_ms):
        if status == 0 or status >= 400:
            failed.append((url, status))
            continue
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            expect(page).to_have_url(url, timeout=30000)
            visited.append(url)
        finally:
            page.close()
    return CrawlResult(visited_urls=visited, failed_urls=failed)


