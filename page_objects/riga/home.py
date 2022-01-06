from __future__ import annotations

from playwright.sync_api import Page, expect
from ..base_page import BasePage


class RigaHomePage(BasePage):
    """Riga.lv home page."""

    def open(self) -> None:  # type: ignore[override]
        super().open("/")

    def open_menu(self) -> None:
        # Try common accessible patterns first
        menu_btn = self.page.get_by_role("button", name=lambda s: "Izvēlne" in s or "Menu" in s)
        if menu_btn.count() > 0:
            menu_btn.first.click()

    def header_links(self) -> int:
        nav = self.page.get_by_role("navigation")
        return nav.get_by_role("link").count()

    def footer_links(self) -> int:
        footer = self.page.locator("footer")
        return footer.locator("a[href]").count()

    def search(self, query: str) -> None:
        # Riga search field can be dynamic; try role=searchbox first
        input_box = self.page.get_by_role("textbox", name=lambda s: "Meklēt" in s or "Search" in s)
        if input_box.count() == 0:
            input_box = self.page.locator("input[type='search'], input[name*='search'], input[name*='mekl']")
        input_box.first.fill(query)
        input_box.first.press("Enter")
        expect(self.page).to_have_url(lambda url: "search" in url or "meklet" in url.lower())

from __future__ import annotations

from playwright.sync_api import Page, expect


class RigaHomePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")

    def heading(self) -> str:
        text = self.page.get_by_role("heading").first.text_content() or ""
        return text.strip()

    def open_menu(self) -> None:
        candidates = ["Izvēlne", "Menu", "Meklēt", "Aizvērt"]
        for name in candidates:
            btn = self.page.get_by_role("button", name=name)
            if btn.count() > 0:
                try:
                    btn.first.click(timeout=1200)
                    return
                except Exception:
                    continue

    def visible_nav_links(self) -> int:
        return self.page.locator("nav a[href]").count()

    def search(self, query: str) -> None:
        box = self.page.get_by_role("textbox", name="Meklēt")
        if box.count() == 0:
            box = self.page.get_by_role("textbox")
        box.first.fill(query)
        box.first.press("Enter")

    def first_link_text(self) -> str:
        a = self.page.locator("a[href]").first
        return (a.text_content() or "").strip()


