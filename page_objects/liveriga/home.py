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


