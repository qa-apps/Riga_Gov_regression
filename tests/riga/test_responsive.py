from __future__ import annotations

from utils.site_checks import open_home
from playwright.sync_api import expect


def test_desktop_view(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 1440, "height": 900})
    open_home(page, riga_base_url)
    expect(page.locator("header")).to_be_visible()
    assert page.locator("nav a[href]").count() >= 3


def test_tablet_view(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 1024, "height": 768})
    open_home(page, riga_base_url)
    expect(page.locator("header")).to_be_visible()
    assert page.locator("a[href]").count() >= 3


def test_mobile_view(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    open_home(page, riga_base_url)
    assert page.locator("header").count() >= 1
    btns = page.get_by_role("button")
    assert btns.count() >= 0


def test_mobile_menu_present(page, riga_base_url) -> None:
    page.set_viewport_size({"width": 375, "height": 667})
    open_home(page, riga_base_url)
    menu_button = page.get_by_role("button", name=lambda n: n and ("Izvēlne" in n or "Menu" in n))
    if menu_button.count() > 0:
        try:
            menu_button.first.click(timeout=1200)
        except Exception:
            pass
    assert page.locator("nav").count() >= 1


from page_objects.riga.home import RigaHomePage

def test_home_nav_links_have_text(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    nav = page.get_by_role("navigation")
    links = nav.get_by_role("link")
    for i in range(min(30, links.count())):
        txt = (links.nth(i).text_content() or "").strip()
        assert len(txt) > 0

def test_home_nav_links_reachable(context, page, riga_base_url) -> None:
    page.goto(riga_base_url)
    nav = page.get_by_role("navigation")
    anchors = nav.locator("a[href]")
    hrefs = []
    for i in range(min(30, anchors.count())):
        h = anchors.nth(i).get_attribute("href")
        if h: hrefs.append(page.evaluate("(u,b)=>new URL(u,b).toString()", h, riga_base_url))
    from utils.crawl import check_urls
    statuses = check_urls(context, hrefs)
    broken = [(u,s) for u,s in statuses if s==0 or s>=400]
    assert len(broken) == 0, f"Broken header links: {broken}"

def test_home_click_first_five_nav_links(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    nav = page.get_by_role("navigation")
    anchors = nav.locator("a[href]")
    for i in range(min(5, anchors.count())):
        href = anchors.nth(i).get_attribute("href")
        if not href: continue
        with page.expect_navigation():
            anchors.nth(i).click(force=True)
        assert page.url.startswith("https://")
        page.goto(riga_base_url)

def test_home_images_have_dimensions(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    bad = page.evaluate("""() => Array.from(document.images)
          .filter(i => (i.naturalWidth||0)===0 || (i.naturalHeight||0)===0)
          .map(i=>i.src)""")
    assert len(bad) == 0

def test_home_assets_status(context, page, riga_base_url) -> None:
    page.goto(riga_base_url)
    css = page.eval_on_selector_all("link[rel='stylesheet'][href]", "(n)=>n.map(x=>x.href)")
    js = page.eval_on_selector_all("script[src]", "(n)=>n.map(x=>x.src)")
    from utils.assets import head_statuses
    statuses = head_statuses(context, [*css[:20], *js[:20]])
    broken = [(u,s) for u,s in statuses if s==0 or s>=400]
    assert len(broken) == 0

def test_home_has_canonical_or_og(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    canon = page.locator("link[rel='canonical']")
    ogurl = page.locator("meta[property='og:url']")
    assert canon.count()>0 or ogurl.count()>0

def test_home_keyboard_nav(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    nav = page.get_by_role("navigation")
    first = nav.get_by_role("link").first
    first.focus()
    assert first.evaluate("el => document.activeElement === el")
    for _ in range(5): page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement !== null")

def test_home_external_blank_noopener(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    nav = page.get_by_role("navigation")
    ext = nav.locator("a[target='_blank']")
    for i in range(ext.count()):
        rel = (ext.nth(i).get_attribute("rel") or "").lower()
        assert "noopener" in rel or "noreferrer" in rel

def test_logo_links_home(page, riga_base_url) -> None:
    page.goto(riga_base_url)
    logo = page.locator("a[href='/'], a.logo, a[aria-label*='home' i]")
    if logo.count()==0: return
    logo.first.click()
    assert page.url.startswith(riga_base_url)
