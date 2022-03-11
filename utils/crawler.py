from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Callable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from playwright.sync_api import BrowserContext, Page, Response
def make_same_domain_filter(base_url: str) -> Callable[[str], bool]:
    def _f(url: str) -> bool:
        return _is_same_domain(url, base_url)
    return _f


def collect_unique_paths(urls: Iterable[str]) -> List[str]:
    seen: Set[str] = set()
    out: List[str] = []
    for u in urls:
        path = urlparse(u).path
        if path not in seen:
            seen.add(path)
            out.append(u)
    return out
def _is_same_domain(url: str, base: str) -> bool:
    p = urlparse(url)
    b = urlparse(base)
    if not p.netloc:
        return True
    if not b.netloc:
        return False
    return p.netloc == b.netloc
def _normalize_link(href: str, base_url: str) -> str:
    if href.startswith("#") or href.startswith("javascript:"):
        return ""
    return urljoin(base_url, href)
def _visible_links(page: Page) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    anchors = page.locator("a[href]")
    count = anchors.count()
    for i in range(count):
        a = anchors.nth(i)
        try:
            if a.is_visible():
                href = a.get_attribute("href") or ""
                name = (a.inner_text() or "").strip()
                items.append((name, href))
        except Exception:
            continue
    return items
def _expand_drop_downs(page: Page) -> None:
    toggles = page.locator("[aria-expanded], [aria-haspopup='true'], .dropdown, .menu, summary")
    count = min(20, toggles.count())
    for i in range(count):
        t = toggles.nth(i)
        try:
            if t.is_visible():
                t.hover()
                time.sleep(0.05)
                t.click(timeout=1200)
        except Exception:
            continue
@dataclass
class CrawlResult:
    visited: List[str]
    failures: List[Tuple[str, str]]
    status_ok: List[Tuple[str, int]]

@dataclass
class CrawlOptions:
    max_pages: int = 30
    delay_ms: int = 0
    include_external: bool = False
    link_filter: Optional[Callable[[str], bool]] = None


def crawl_site(
    context: BrowserContext,
    base_url: str,
    max_pages: int = 30,
    options: Optional[CrawlOptions] = None,
) -> CrawlResult:
    opts = options or CrawlOptions(max_pages=max_pages)
    page = context.new_page()
    visited: Set[str] = set()
    failures: List[Tuple[str, str]] = []
    status_ok: List[Tuple[str, int]] = []
    queue: List[str] = [base_url]
    while queue and len(visited) < opts.max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            resp = page.goto(url, wait_until="domcontentloaded")
        except Exception as e:
            failures.append((url, f"navigation error: {e!r}"))
            continue

        status = resp.status if isinstance(resp, Response) else 0
        if 200 <= status < 400:
            status_ok.append((url, status))
        else:
            failures.append((url, f"bad status: {status}"))

        _expand_drop_downs(page)
        links = _visible_links(page)
        for _, href in links:
            target = _normalize_link(href, url)
            if not target:
                continue
            if not opts.include_external and not _is_same_domain(target, base_url):
                continue
            if opts.link_filter and not opts.link_filter(target):
                continue
            if target not in visited and target not in queue:
                queue.append(target)

        if opts.delay_ms > 0:
            time.sleep(opts.delay_ms / 1000.0)

    page.close()
    return CrawlResult(visited=list(visited), failures=failures, status_ok=status_ok)

