from __future__ import annotations

from playwright.sync_api import Page, expect
from ..base_page import BasePage


class LiveRigaHomePage(BasePage):
    """LiveRiga home page."""

    def open(self) -> None:  # type: ignore[override]
        super().open("/")

    def open_menu(self) -> None:
        menu_btn = self.page.get_by_role("button", name=lambda s: "Menu" in s or "Izvēlne" in s)
        if menu_btn.count() > 0:
            menu_btn.first.click()

    def search(self, query: str) -> None:
        input_box = self.page.get_by_role("textbox", name=lambda s: "Search" in s or "Meklēt" in s)
        if input_box.count() == 0:
            input_box = self.page.locator("input[type='search'], input[name*='search']")
        input_box.first.fill(query)
        input_box.first.press("Enter")
        expect(self.page).to_have_url(lambda u: "search" in u or "mekl" in u.lower())

from __future__ import annotations
from playwright.sync_api import Page


class LiveRigaHomePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")

    def open_menu(self) -> None:
        btns = self.page.get_by_role("button")
        count = min(10, btns.count())
        for i in range(count):
            b = btns.nth(i)
            label = (b.get_attribute("aria-label") or "").lower()
            name = (b.text_content() or "").lower()
            if "menu" in name or "izvēlne" in name or "menu" in label:
                try:
                    b.click(timeout=1200)
                    return
                except Exception:
                    continue


