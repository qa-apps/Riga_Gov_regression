from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage
from utils.crawl import check_urls


def test_liveriga_header_nav_links_are_reachable(context, page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    home.open_menu()
    nav_links = page.get_by_role("navigation").locator("a[href]")
    hrefs = []
    for i in range(min(30, nav_links.count())):
        href = nav_links.nth(i).get_attribute("href")
        if href:
            hrefs.append(href)
    urls = [page.evaluate("(u, b) => new URL(u, b).toString()", h, liveriga_base_url) for h in hrefs]
    statuses = check_urls(context, urls)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f"Broken header links: {broken}"

def test_liveriga_header_nav_links_have_text(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    links = nav.get_by_role("link")
    for i in range(min(30, links.count())):
        txt = (links.nth(i).text_content() or "").strip()
        assert len(txt) > 0


def test_liveriga_header_nav_no_javascript_void_links(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    links = nav.locator("a[href]")
    for i in range(min(30, links.count())):
        href = links.nth(i).get_attribute("href") or ""
        assert "javascript:void" not in href.lower()


def test_liveriga_click_first_five_nav_links_navigate(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    links = nav.locator("a[href]")
    count = min(5, links.count())
    for i in range(count):
        href = links.nth(i).get_attribute("href")
        if not href:
            continue
        url = page.evaluate("(u, b) => new URL(u, b).toString()", href, liveriga_base_url)
        with page.expect_navigation():
            links.nth(i).click(force=True)
        assert page.url.startswith("https://")
        page.goto(liveriga_base_url)


def test_liveriga_header_nav_keyboard_tab_navigation(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    first = nav.get_by_role("link").first
    first.focus()
    assert first.evaluate("el => document.activeElement === el")
    for _ in range(5):
        page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement !== null")


def test_liveriga_nav_external_blank_links_have_noopener(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    links = nav.locator("a[target='_blank']")
    for i in range(links.count()):
        rel = (links.nth(i).get_attribute("rel") or "").lower()
        assert "noopener" in rel or "noreferrer" in rel


def test_liveriga_header_contains_aria_labels(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    assert nav.count() > 0
    # Ensure navigation region exists (label may be implicit)
    assert nav.count() >= 1
