from __future__ import annotations

import pytest
from pathlib import Path


def test_readme_has_usage_sections() -> None:
    p = Path("README.md")
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "Environment variables" in text and "Running by site and markers" in text


