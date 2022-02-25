from __future__ import annotations

import pytest
from playwright.sync_api import expect

from page_objects.riga.home import RigaHomePage
from utils.a11y import run_axe


@pytest.mark.a11y
def test_riga_homepage_has_no_critical_violations(page, riga_base_url) -> None:
    home = RigaHomePage(page, riga_base_url)
    home.open()
    violations = run_axe(page)
    critical = [v for v in violations if v.get("impact") in {"critical"}]
    assert len(critical) == 0, f"Critical a11y issues: {critical}"


