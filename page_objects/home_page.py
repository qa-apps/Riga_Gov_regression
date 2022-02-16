from __future__ import annotations

from playwright.sync_api import Page
from .base_page import BasePage


class HomePage(BasePage):
    """Home page object."""

    def __init__(self, page: Page, base_url: str) -> None:
        """Create the home page object."""
        super().__init__(page, base_url)

    def open(self) -> None:  # type: ignore[override]
        """Open the homepage."""
        super().open("/")

    def heading_text(self) -> str:
        """Return main page heading text."""
        return self.get_text("h1")


