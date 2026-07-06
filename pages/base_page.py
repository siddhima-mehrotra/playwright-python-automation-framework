"""
base_page.py — Base Page Object
All page objects inherit from this class for shared browser actions.
"""

from playwright.sync_api import Page, expect
from utils.logger import get_logger
from utils.retry import retry

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ── Navigation ──────────────────────────────────────────────────────────

    def navigate(self, url: str):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    # ── Element Actions ──────────────────────────────────────────────────────

    @retry(max_attempts=3, delay=1)
    def click(self, selector: str):
        logger.info(f"Clicking: {selector}")
        self.page.locator(selector).click()

    @retry(max_attempts=3, delay=1)
    def fill(self, selector: str, value: str):
        logger.info(f"Filling '{selector}' with value")
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_selector(self, selector: str, timeout: int = 10000):
        self.page.wait_for_selector(selector, timeout=timeout)

    # ── Assertions ───────────────────────────────────────────────────────────

    def assert_url_contains(self, text: str):
        expect(self.page).to_have_url(lambda url: text in url)

    def assert_element_visible(self, selector: str):
        expect(self.page.locator(selector)).to_be_visible()

    def assert_text(self, selector: str, expected_text: str):
        expect(self.page.locator(selector)).to_have_text(expected_text)

    # ── Utilities ────────────────────────────────────────────────────────────

    def take_screenshot(self, name: str):
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        logger.info(f"Screenshot saved: {path}")
        return path

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
