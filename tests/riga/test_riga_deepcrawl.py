from __future__ import annotations

import pytest

from utils.deepcrawl import deep_crawl


@pytest.mark.smoke
def test_riga_deep_crawl_visits_many_pages(context, riga_base_url) -> None:
    result = deep_crawl(context, riga_base_url, max_pages=40, max_depth=2)
    # Require that we reach at least 20 pages without failures
    assert len(result.visited) >= 20
    assert len(result.failures) == 0, f"Failures during crawl: {result.failures[:10]}"


