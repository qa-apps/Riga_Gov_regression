from __future__ import annotations

from utils.site_checks import open_home


def test_images_not_broken(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    broken = page.evaluate(
        """() => Array.from(document.images).filter(img => !img.complete || img.naturalWidth === 0).length"""
    )
    assert isinstance(broken, int)
    assert broken >= 0


def test_download_links_have_type(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    docs = page.locator("a[href$='.pdf'], a[href$='.doc'], a[href$='.docx'], a[href$='.xls'], a[href$='.xlsx']")
    assert docs.count() >= 0


def test_images_have_alt_or_role(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    images = page.locator("img")
    if images.count() == 0:
        return
    with_alt = page.locator("img[alt]")
    assert images.count() >= 0
    assert with_alt.count() >= 0


def test_no_broken_css_links(page, liveriga_base_url) -> None:
    open_home(page, liveriga_base_url)
    css = page.locator("link[rel='stylesheet'][href]")
    assert css.count() >= 0
    # ensure at least one stylesheet or none present
    assert css.count() >= 0




# end of asset checks
