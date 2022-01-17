from __future__ import annotations
import re
from typing import Dict, List, Optional, Tuple
from playwright.sync_api import BrowserContext, Page, expect


def accept_cookies_if_present(page: Page) -> None:
    candidates = [
        "Piekrītu",
        "Apstiprināt",
        "Akceptēt",
        "I agree",
        "Accept",
        "Allow all",
    ]
    for text in candidates:
        try:
            btn = page.get_by_role("button", name=re.compile(text, re.I))
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(timeout=1500)
                return
        except Exception:
            continue
    try:
        page.locator("[data-accept], .cookie-accept, .cc-allow-all, .cookie-yes").first.click(timeout=1200)
    except Exception:
        pass


def open_home(page: Page, base_url: str) -> None:
    page.goto(base_url, wait_until="domcontentloaded")
    accept_cookies_if_present(page)


def check_security_headers(context: BrowserContext, url: str) -> Dict[str, Optional[str]]:
    resp = context.request.get(url)
    headers = {k.lower(): v for k, v in resp.headers.items()}
    required = [
        "content-security-policy",
        "strict-transport-security",
        "x-content-type-options",
        "referrer-policy",
        "permissions-policy",
    ]
    results: Dict[str, Optional[str]] = {}
    for h in required:
        results[h] = headers.get(h)
    return results


def external_link_is_safe(page: Page, selector: str) -> bool:
    a = page.locator(selector).first
    if a.count() == 0:
        return True
    rel = a.get_attribute("rel") or ""
    target = a.get_attribute("target") or ""
    return ("noopener" in rel and "noreferrer" in rel) or target != "_blank"


