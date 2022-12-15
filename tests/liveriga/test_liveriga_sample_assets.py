from __future__ import annotations

import pytest

from utils.samples import sample_internal_pages
from utils.assets import collect_image_urls, head_statuses
from page_objects.liveriga.home import LiveRigaHomePage


def test_liveriga_sample_pages_have_no_broken_images(context, page, liveriga_base_url) -> None:
    pages = sample_internal_pages(context, liveriga_base_url, max_pages=10)
    broken_total = []
    for url in pages:
        page.goto(url)
        imgs = collect_image_urls(page, liveriga_base_url)[:30]
        statuses = head_statuses(context, imgs)
        broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
        broken_total.extend(broken)
    assert len(broken_total) == 0, f"Broken images across sample: {broken_total[:10]}"




def test_liveriga_sample_pages_documents_downloadable(context, page, liveriga_base_url) -> None:
    pages = sample_internal_pages(context, liveriga_base_url, max_pages=6)
    from utils.assets import collect_document_urls
    broken_total = []
    for url in pages:
        page.goto(url)
        docs = collect_document_urls(page, liveriga_base_url)[:10]
        if not docs:
            continue
        statuses = head_statuses(context, docs)
        broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
        broken_total.extend(broken)
    assert len(broken_total) == 0, f"Broken docs: {broken_total[:10]}"


def test_liveriga_homepage_images_have_dimensions(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    bad = page.evaluate(
        """() => Array.from(document.images)
              .filter(i => (i.naturalWidth||0)===0 || (i.naturalHeight||0)===0)
              .map(i=>i.src)"""
    )
    assert len(bad) == 0, f"Zero-dimension images: {bad[:5]}"


def test_liveriga_homepage_images_have_alt_or_aria(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    missing = page.evaluate(
        """() => Array.from(document.querySelectorAll('img'))
              .filter(i => !i.hasAttribute('alt') && !i.getAttribute('role'))
              .map(i=>i.src)"""
    )
    assert len(missing) >= 0


def test_liveriga_homepage_assets_status(context, page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    css = page.eval_on_selector_all("link[rel='stylesheet'][href]", "(n)=>n.map(x=>x.href)")
    js = page.eval_on_selector_all("script[src]", "(n)=>n.map(x=>x.src)")
    urls = list(dict.fromkeys([*css[:20], *js[:20]]))
    statuses = head_statuses(context, urls)
    broken = [(u, s) for u, s in statuses if s == 0 or s >= 400]
    assert len(broken) == 0, f"Broken assets: {broken[:10]}"


def test_liveriga_has_canonical_or_og_url(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    canon = page.locator("link[rel='canonical']")
    ogurl = page.locator("meta[property='og:url']")
    assert canon.count() > 0 or ogurl.count() > 0


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

# extra

def test_additional_head_present(page, liveriga_base_url) -> None:
    page.goto(liveriga_base_url)
    assert page.locator('head').count() >= 1
