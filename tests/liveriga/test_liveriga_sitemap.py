from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest
from playwright.sync_api import expect

from page_objects.liveriga.home import LiveRigaHomePage


@pytest.mark.smoke
def test_liveriga_sitemap_xml_exists_and_parses(context, liveriga_base_url) -> None:
    url = liveriga_base_url.rstrip("/") + "/sitemap.xml"
    resp = context.request.get(url, timeout=20000)
    assert resp.ok, f"Failed sitemap status {resp.status}"
    root = ET.fromstring(resp.text())
    assert root.tag.endswith("sitemapindex") or root.tag.endswith("urlset")


def test_liveriga_first_sitemap_entry_is_reachable(context, liveriga_base_url, browser) -> None:
    url = liveriga_base_url.rstrip("/") + "/sitemap.xml"
    resp = context.request.get(url, timeout=20000)
    root = ET.fromstring(resp.text())
    ns_loc = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
    loc_text = None
    for tag in ("sitemap", "url"):
        for node in root.findall(f".//{{*}}{tag}"):
            loc = node.find(f".//{{*}}loc") or node.find(ns_loc)
            if loc is not None and loc.text:
                loc_text = loc.text.strip()
                break
        if loc_text:
            break
    assert loc_text
    page = browser.new_page()
    page.goto(loc_text, wait_until="domcontentloaded")
    expect(page.get_by_role("main")).to_be_visible()
    page.close()


