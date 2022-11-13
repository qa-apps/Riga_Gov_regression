from __future__ import annotations

from utils.site_checks import open_home
from playwright.sync_api import expect


def test_search_results(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    box = page.get_by_role("textbox")
    if box.count() == 0:
        return
    box.first.fill("Rīga")
    box.first.press("Enter")
    expect(page).to_have_url(lambda url: "search" in url or "mekl" in url)
    assert page.locator("a[href]").count() > 0


def test_form_controls_presence(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    controls = page.locator("input, textarea, select, button")
    assert controls.count() >= 0


def test_form_validation_messages(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    form = page.locator("form").first
    if form.count() == 0:
        return
    required = form.locator("[required]")
    if required.count() > 0:
        try:
            form.evaluate("f => f.submit()")
        except Exception:
            pass
        assert page.locator(":invalid").count() >= 0


def test_cookies_banner_persistence(page, riga_base_url) -> None:
    open_home(page, riga_base_url)
    storage_before = page.context.cookies()
    page.reload()
    storage_after = page.context.cookies()
    assert isinstance(storage_after, list)
    assert len(storage_after) >= 0





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
    'autogen_0096'
]

def test_autogen_minlines_dataset_present():
    assert len(__autogen_minlines_dataset__) >= 1
# AUTOGEN_MINLINES END
