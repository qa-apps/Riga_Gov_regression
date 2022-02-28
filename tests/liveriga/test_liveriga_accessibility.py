from __future__ import annotations

import pytest

from page_objects.liveriga.home import LiveRigaHomePage
from utils.a11y import run_axe


@pytest.mark.a11y
def test_liveriga_homepage_has_no_critical_violations(page, liveriga_base_url) -> None:
    home = LiveRigaHomePage(page, liveriga_base_url)
    home.open()
    violations = run_axe(page)
    critical = [v for v in violations if v.get(\"impact\") in {\"critical\"}]
    assert len(critical) == 0, f\"Critical a11y issues: {critical}\"


