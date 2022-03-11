from __future__ import annotations

from typing import Iterable, List, Tuple
from urllib.parse import urljoin, urlparse

from playwright.sync_api import BrowserContext, Page


def collect_image_urls(page: Page, base_url: str) -> List[str]:
    """Collect fully-qualified image URLs from img[src]."""
    items = page.eval_on_selector_all(
        "img[src]", "(nodes) => nodes.map(n => n.getAttribute('src'))"
    )
    urls = []
    for src in items:
        if not src:
            continue
        urls.append(urljoin(base_url, src))
    return urls


def collect_document_urls(page: Page, base_url: str) -> List[str]:
    """Collect URLs likely pointing to downloadable documents."""
    exts = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx")
    items = page.eval_on_selector_all(
        "a[href]", "(nodes) => nodes.map(n => n.getAttribute('href'))"
    )
    urls = []
    for href in items:
        if not href:
            continue
        if href.lower().endswith(exts):
            urls.append(urljoin(base_url, href))
    return urls


def head_statuses(context: BrowserContext, urls: Iterable[str]) -> List[Tuple[str, int]]:
    """Attempt HEAD then GET if HEAD not allowed, return statuses."""
    statuses: List[Tuple[str, int]] = []
    for url in urls:
        try:
            resp = context.request.fetch(url, method="HEAD", timeout=20000)
            statuses.append((url, resp.status))
        except Exception:
            try:
                resp = context.request.get(url, timeout=20000)
                statuses.append((url, resp.status))
            except Exception:
                statuses.append((url, 0))
    return statuses


