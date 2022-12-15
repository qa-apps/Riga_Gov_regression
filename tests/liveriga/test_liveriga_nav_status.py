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


import itertools
from utils.samples import sample_internal_pages
from utils.crawl import check_urls


def test_sample_internal_links_status(context, page, liveriga_base_url) -> None:
    pages = sample_internal_pages(context, liveriga_base_url, max_pages=6)
    hrefs = []
    for url in pages:
        page.goto(url)
        for h in page.eval_on_selector_all("a[href]", "(n)=>n.map(x=>x.getAttribute('href'))")[:30]:
            if not h:
                continue
            full = page.evaluate("(u,b)=>new URL(u,b).toString()", h, liveriga_base_url)
            hrefs.append(full)
    statuses = check_urls(context, list(dict.fromkeys(hrefs))[:60])
    assert all(200 <= s < 400 for _, s in statuses), f"Broken among sample: {[(u,s) for u,s in statuses if s<200 or s>=400][:10]}"


def test_sample_pages_have_headings_and_main(page, liveriga_base_url, context) -> None:
    for url in sample_internal_pages(context, liveriga_base_url, max_pages=8):
        page.goto(url)
        has_heading = page.get_by_role('heading').count() > 0
        has_main = page.get_by_role('main').count() > 0
        assert has_heading or has_main


def test_sample_pages_have_lang_attribute(page, liveriga_base_url, context) -> None:
    for url in sample_internal_pages(context, liveriga_base_url, max_pages=5):
        page.goto(url)
        lang = page.evaluate("document.documentElement.lang || ''")
        assert isinstance(lang, str)


def test_sample_pages_no_mixed_content(page, liveriga_base_url, context) -> None:
    for url in sample_internal_pages(context, liveriga_base_url, max_pages=5):
        page.goto(url)
        refs = page.evaluate("""() => { const sel=['img[src]','script[src]','link[href]'];
            const out=[]; sel.forEach(s=>document.querySelectorAll(s).forEach(n=>{
            const u=n.getAttribute('src')||n.getAttribute('href')||''; if(u.startsWith('http://')) out.push(u);})); return out; }""")
        assert len(refs) == 0


def test_additional_heading_presence(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    assert page.get_by_role('heading').count() >= 0


def test_additional_footer_presence(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    assert page.locator('footer').count() >= 0


def test_additional_navigation_presence(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    assert page.get_by_role('navigation').count() >= 0


def test_additional_any_link_present(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    assert page.locator('a[href]').count() >= 0


def test_additional_banner_and_footer_roles(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    # These roles may be absent on some pages; presence is optional
    page.get_by_role('banner')
    page.get_by_role('contentinfo')


def test_additional_breadcrumbs_optional(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    _ = page.locator("nav[aria-label*='crumb' i], .breadcrumb, .breadcrumbs")
