from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

from playwright.sync_api import BrowserContext


def same_host(a: str, b: str) -> bool:
    return urlparse(a).netloc == urlparse(b).netloc


def normalize(href: str, base: str) -> str:
    if not href:
        return ""
    return urljoin(base, href)


def extract_links(context: BrowserContext, url: str, base: str) -> List[str]:
    page = context.new_page()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        hrefs = page.eval_on_selector_all(
            "a[href]",
            "(nodes) => nodes.map(n => n.getAttribute('href'))",
        )
        urls: List[str] = []
        for h in hrefs:
            full = normalize(h or "", base)
            if full and same_host(full, base):
                urls.append(full.split('#', 1)[0])
        return list(dict.fromkeys(urls))
    finally:
        page.close()


@dataclass
class DeepCrawlResult:
    visited: List[str]
    failures: List[Tuple[str, int]]


def deep_crawl(
    context: BrowserContext,
    start_url: str,
    max_pages: int = 60,
    max_depth: int = 2,
) -> DeepCrawlResult:
    """Breadth-first crawl up to max_pages within max_depth from start_url."""
    queue: Deque[Tuple[str, int]] = deque([(start_url, 0)])
    seen: Set[str] = set([start_url])
    visited: List[str] = []
    failures: List[Tuple[str, int]] = []
    base = start_url
    while queue and len(visited) < max_pages:
        url, depth = queue.popleft()
        try:
            resp = context.request.get(url, timeout=20000)
            status = resp.status
        except Exception:
            status = 0
        if status == 0 or status >= 400:
            failures.append((url, status))
            continue
        visited.append(url)
        if depth >= max_depth:
            continue
        for link in extract_links(context, url, base):
            if link not in seen:
                seen.add(link)
                queue.append((link, depth + 1))
                if len(seen) >= max_pages * 3:
                    break
    return DeepCrawlResult(visited=visited, failures=failures)


