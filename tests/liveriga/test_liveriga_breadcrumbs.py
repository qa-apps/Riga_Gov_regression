from __future__ import annotations

import pytest
from playwright.sync_api import expect

from utils.samples import sample_internal_pages
from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_sample_pages_expose_breadcrumbs_semantics(page, liveriga_base_url, context) -> None:
    pages = sample_internal_pages(context, liveriga_base_url, max_pages=8)
    has_crumbs = False
    for url in pages:
        page.goto(url)
        crumbs = page.locator("nav[aria-label*='crumb' i], .breadcrumb, .breadcrumbs")
        if crumbs.count() > 0:
            has_crumbs = True
            expect(crumbs).to_be_visible()
            break
    assert has_crumbs, \"No breadcrumbs semantics found in sampled pages\"


def test_home_nav_links_have_text(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    links = nav.get_by_role("link")
    for i in range(min(30, links.count())):
        txt = (links.nth(i).text_content() or "").strip()
        assert len(txt) > 0

def test_home_nav_links_reachable(context, page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    anchors = nav.locator("a[href]")
    hrefs = []
    for i in range(min(30, anchors.count())):
        h = anchors.nth(i).get_attribute("href")
        if h: hrefs.append(page.evaluate("(u,b)=>new URL(u,b).toString()", h, liveriga_base_url))
    from utils.crawl import check_urls
    statuses = check_urls(context, hrefs)
    broken = [(u,s) for u,s in statuses if s==0 or s>=400]
    assert len(broken) == 0, f"Broken header links: {broken}"

def test_home_click_first_five_nav_links(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    anchors = nav.locator("a[href]")
    for i in range(min(5, anchors.count())):
        href = anchors.nth(i).get_attribute("href")
        if not href: continue
        with page.expect_navigation():
            anchors.nth(i).click(force=True)
        assert page.url.startswith("https://")
        page.goto(liveriga_base_url)

def test_home_images_have_dimensions(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    bad = page.evaluate("""() => Array.from(document.images)
          .filter(i => (i.naturalWidth||0)===0 || (i.naturalHeight||0)===0)
          .map(i=>i.src)""")
    assert len(bad) == 0

def test_home_assets_status(context, page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    css = page.eval_on_selector_all("link[rel='stylesheet'][href]", "(n)=>n.map(x=>x.href)")
    js = page.eval_on_selector_all("script[src]", "(n)=>n.map(x=>x.src)")
    from utils.assets import head_statuses
    statuses = head_statuses(context, [*css[:20], *js[:20]])
    broken = [(u,s) for u,s in statuses if s==0 or s>=400]
    assert len(broken) == 0

def test_home_has_canonical_or_og(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    canon = page.locator("link[rel='canonical']")
    ogurl = page.locator("meta[property='og:url']")
    assert canon.count()>0 or ogurl.count()>0

def test_home_keyboard_nav(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    first = nav.get_by_role("link").first
    first.focus()
    assert first.evaluate("el => document.activeElement === el")
    for _ in range(5): page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement !== null")

def test_home_external_blank_noopener(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    nav = page.get_by_role("navigation")
    ext = nav.locator("a[target='_blank']")
    for i in range(ext.count()):
        rel = (ext.nth(i).get_attribute("rel") or "").lower()
        assert "noopener" in rel or "noreferrer" in rel

def test_logo_links_home(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    logo = page.locator("a[href='/'], a.logo, a[aria-label*='home' i]")
    if logo.count()==0: return
    logo.first.click()
    assert page.url.startswith(liveriga_base_url)
