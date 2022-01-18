from __future__ import annotations
from playwright.sync_api import Page


class RigaHeader:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open_mobile_menu(self) -> None:
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

    def nav_links_count(self) -> int:
        return self.page.locator("header nav a[href]").count()


