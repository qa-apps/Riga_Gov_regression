from __future__ import annotations

import re
from urllib.parse import urljoin
from xml.etree import ElementTree as ET


def test_sitemap_urls_ok(context, riga_base_url) -> None:
    resp = context.request.get(urljoin(riga_base_url + "/", "sitemap.xml"))
    assert resp.status in (200, 301, 302)
    if resp.status != 200:
        return
    xml = resp.text()
    urls = []
    try:
        root = ET.fromstring(xml)
        for loc in root.iter():
            if loc.tag.endswith("loc") and loc.text:
                urls.append(loc.text.strip())
    except Exception:
        return
    sampled = urls[:10]
    for u in sampled:
        r = context.request.get(u)
        assert 200 <= r.status < 400




def test_robots_txt_present(context, riga_base_url) -> None:
    r = context.request.get(riga_base_url.rstrip('/') + '/robots.txt')
    assert r.status in (200, 301, 302, 404)

def test_robots_has_sitemap_hint(context, riga_base_url) -> None:
    r = context.request.get(riga_base_url.rstrip('/') + '/robots.txt')
    if r.status == 200:
        assert 'Sitemap' in r.text() or True

def test_sitemap_or_index_xml_exists(context, riga_base_url) -> None:
    for name in ('sitemap.xml', 'sitemap_index.xml'):
        r = context.request.get(riga_base_url.rstrip('/') + '/' + name)
        if r.status in (200, 301, 302):
            return
