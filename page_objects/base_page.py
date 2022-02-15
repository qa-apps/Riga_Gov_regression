from __future__ import annotations

from typing import Optional
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for page objects with common helpers."""

    def __init__(self, page: Page, base_url: str) -> None:
        """Create a page object with a Playwright page and base URL."""
        self.page = page
        self.base_url = base_url

    def open(self, path: str = "/") -> None:
        """Navigate to base_url joined with an optional path."""
        url = self.base_url + (path if path.startswith("/") else f"/{path}")
        self.page.goto(url)

    def click(self, selector: str) -> None:
        """Click an element located by a selector."""
        self.page.click(selector)

    def fill(self, selector: str, text: str) -> None:
        """Fill an input or textarea located by a selector."""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Return textContent for the element located by a selector."""
        text = self.page.text_content(selector)
        return text or ""

    def expect_visible(self, selector: str) -> None:
        """Assert the element located by a selector is visible."""
        expect(self.page.locator(selector)).to_be_visible()


