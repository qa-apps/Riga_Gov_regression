from __future__ import annotations

import os
import xml.etree.ElementTree as ET

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage


@pytest.mark.smoke
def test_riga_sitemap_xml_exists_and_parses(context, riga_base_url) -> None:
    url = riga_base_url.rstrip("/") + "/sitemap.xml"
    resp = context.request.get(url, timeout=20000)
    assert resp.ok, f"Failed sitemap status {resp.status}"
    # Parse XML
    root = ET.fromstring(resp.text())
    # Accept both sitemapindex and urlset roots
    assert root.tag.endswith("sitemapindex") or root.tag.endswith("urlset")


def test_riga_first_sitemap_entry_is_reachable(context, riga_base_url, browser) -> None:
    url = riga_base_url.rstrip("/") + "/sitemap.xml"
    resp = context.request.get(url, timeout=20000)
    root = ET.fromstring(resp.text())
    # Find first loc under either <sitemap> or <url>
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
    # Navigate to ensure it's reachable
    page = browser.new_page()
    page.goto(loc_text, wait_until="domcontentloaded")
    expect(page.get_by_role("main")).to_be_visible()
    page.close()


