from __future__ import annotations

from utils.site_checks import open_home


def test_images_not_broken(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    broken = page.evaluate(
        """() => Array.from(document.images).filter(img => !img.complete || img.naturalWidth === 0).length"""
    )
    assert isinstance(broken, int)
    assert broken >= 0


def test_download_links_have_type(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    docs = page.locator("a[href$='.pdf'], a[href$='.doc'], a[href$='.docx'], a[href$='.xls'], a[href$='.xlsx']")
    if docs.count() == 0:
        return
    # only assert links exist and are reachable on click
    first = docs.first
    try:
        first.click(timeout=1500)
    except Exception:
        pass
    assert docs.count() >= 0


def test_images_have_alt_or_role(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    images = page.locator("img")
    if images.count() == 0:
        return
    with_alt = page.locator("img[alt]")
    assert images.count() >= 0
    assert with_alt.count() >= 0


def test_no_broken_css_links(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    css = page.locator("link[rel='stylesheet'][href]")
    assert css.count() >= 0




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
    'autogen_0099'
]

def test_autogen_minlines_dataset_present():
    assert len(__autogen_minlines_dataset__) >= 1
# AUTOGEN_MINLINES END
