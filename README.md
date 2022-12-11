## Playwright + Python Test Framework

Minimal pytest-based UI test framework using Playwright and the Page Object Model.

### Setup

1) Python 3.10+ recommended.
2) Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows (PowerShell)
```

3) Install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install
```

4) Configure environment (optional):
- Create a `.env` file in the project root with:
  - `BASE_URL=https://example.com`
  - `LOCALE=en-US`
  - `TIMEZONE_ID=UTC`
  - `PW_VIDEO_DIR=test-results/videos`

### Run tests

```bash
pytest
```

Useful options:
- Headed mode: `pytest --headed`
- Choose browser: `pytest --browser chromium` (chromium|firefox|webkit)
- Tracing (local): `pytest --trace on-first-retry`

### Project layout

- `tests/` — test suites
- `page_objects/` — page object models
- `conftest.py` — shared fixtures and env handling
- `pytest.ini` — pytest configuration

### Environment variables

- `RIGA_BASE_URL` default `https://www.riga.lv`
- `LIVERIGA_BASE_URL` default `https://www.liveriga.com/lv`
- `PW_VIDEO_DIR` directory for Playwright videos
- `LOCALE`, `TIMEZONE_ID` used by context

### Running by site and markers

```bash
# Only Riga tests
pytest tests/riga -q

# Only LiveRiga tests
pytest tests/liveriga -q

# Security checks
pytest -m security -q

# Accessibility checks
pytest -m a11y -q
```

### Notes

- Crawlers restrict to in-domain links and throttle requests to avoid overloading servers.
- External links with target=_blank are checked for `rel=\"noopener\"` or `rel=\"noreferrer\"`.



