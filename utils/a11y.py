from __future__ import annotations

from typing import Any, Dict, List
from playwright.sync_api import Page

AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js"


def inject_axe(page: Page) -> None:
    """Inject axe-core into the current page."""
    page.add_script_tag(url=AXE_CDN)


def run_axe(page: Page, include: str = "body") -> List[Dict[str, Any]]:
    """Run axe-core and return violations."""
    inject_axe(page)
    page.wait_for_timeout(100)  # allow script to initialize
    return page.evaluate(
        """async (selector) => {
            const context = { include: [selector] };
            const options = {};
            const results = await axe.run(context, options);
            return results.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length }));
        }""",
        include,
    )


