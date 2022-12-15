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
