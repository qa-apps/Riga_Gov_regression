from __future__ import annotations

import os
from typing import Any, Dict

import pytest
from dotenv import load_dotenv

# Load variables from .env if present
load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for tests from env or default to example.com."""
    url = os.getenv("BASE_URL", "https://example.com").rstrip("/")
    return url


@pytest.fixture(scope="session")
def riga_base_url() -> str:
    """Base URL for riga.lv tests."""
    return os.getenv("RIGA_BASE_URL", "https://www.riga.lv").rstrip("/")


@pytest.fixture(scope="session")
def liveriga_base_url() -> str:
    """Base URL for liveriga.com/lv tests."""
    return os.getenv("LIVERIGA_BASE_URL", "https://www.liveriga.com/lv").rstrip("/")


@pytest.fixture(scope="session")
def crawl_limit() -> int:
    """Maximum pages to crawl per test (env override)."""
    try:
        return int(os.getenv("CRAWL_LIMIT", "40"))
    except ValueError:
        return 40


@pytest.fixture(scope="session")
def browser_context_args() -> Dict[str, Any]:
    """Configure Playwright browser context via pytest-playwright hook."""
    record_video_dir = os.getenv("PW_VIDEO_DIR", "test-results/videos")
    locale = os.getenv("LOCALE", "en-US")
    timezone_id = os.getenv("TIMEZONE_ID", "UTC")
    return {
        "ignore_https_errors": True,
        "viewport": {"width": 1280, "height": 800},
        "record_video_dir": record_video_dir,
        "locale": locale,
        "timezone_id": timezone_id,
    }


