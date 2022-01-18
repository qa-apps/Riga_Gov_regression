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


