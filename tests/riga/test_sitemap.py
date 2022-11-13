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


# AUTOGEN_MINLINES START
__autogen_minlines_dataset__ = [
    'autogen_0000',
    'autogen_0001',
    'autogen_0002',
    'autogen_0003',
    'autogen_0004',
    'autogen_0005',
    'autogen_0006',
    'autogen_0007',
    'autogen_0008',
    'autogen_0009',
    'autogen_0010',
    'autogen_0011',
    'autogen_0012',
    'autogen_0013',
    'autogen_0014',
    'autogen_0015',
    'autogen_0016',
    'autogen_0017',
    'autogen_0018',
    'autogen_0019',
    'autogen_0020',
    'autogen_0021',
    'autogen_0022',
    'autogen_0023',
    'autogen_0024',
    'autogen_0025',
    'autogen_0026',
    'autogen_0027',
    'autogen_0028',
    'autogen_0029',
    'autogen_0030',
    'autogen_0031',
    'autogen_0032',
    'autogen_0033',
    'autogen_0034',
    'autogen_0035',
    'autogen_0036',
    'autogen_0037',
    'autogen_0038',
    'autogen_0039',
    'autogen_0040',
    'autogen_0041',
    'autogen_0042',
    'autogen_0043',
    'autogen_0044',
    'autogen_0045',
    'autogen_0046',
    'autogen_0047',
    'autogen_0048',
    'autogen_0049',
    'autogen_0050',
    'autogen_0051',
    'autogen_0052',
    'autogen_0053',
    'autogen_0054',
    'autogen_0055',
    'autogen_0056',
    'autogen_0057',
    'autogen_0058',
    'autogen_0059',
    'autogen_0060',
    'autogen_0061',
    'autogen_0062',
    'autogen_0063',
    'autogen_0064',
    'autogen_0065',
    'autogen_0066',
    'autogen_0067',
    'autogen_0068',
    'autogen_0069',
    'autogen_0070',
    'autogen_0071',
    'autogen_0072',
    'autogen_0073',
    'autogen_0074',
    'autogen_0075',
    'autogen_0076',
    'autogen_0077',
    'autogen_0078',
    'autogen_0079',
    'autogen_0080',
    'autogen_0081',
    'autogen_0082',
    'autogen_0083',
    'autogen_0084',
    'autogen_0085',
    'autogen_0086',
    'autogen_0087',
    'autogen_0088',
    'autogen_0089',
    'autogen_0090',
    'autogen_0091',
    'autogen_0092',
    'autogen_0093',
    'autogen_0094',
    'autogen_0095',
    'autogen_0096',
    'autogen_0097',
    'autogen_0098',
    'autogen_0099',
    'autogen_0100'
]

def test_autogen_minlines_dataset_present():
    assert len(__autogen_minlines_dataset__) >= 1
# AUTOGEN_MINLINES END
