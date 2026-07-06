"""
login_page.py — Login Page Object
Encapsulates all login-related UI interactions.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):

    # ── Selectors ────────────────────────────────────────────────────────────
    EMAIL_INPUT    = "[data-testid='email']"
    PASSWORD_INPUT = "[data-testid='password']"
    LOGIN_BUTTON   = "[data-testid='login-btn']"
    ERROR_MESSAGE  = "[data-testid='error-message']"
    WELCOME_HEADER = "h1.welcome"

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/login"

    # ── Actions ──────────────────────────────────────────────────────────────

    def open(self):
        self.navigate(self.url)
        logger.info("Login page opened.")

    def enter_email(self, email: str):
        self.fill(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        """Full login flow — enter credentials and submit."""
        logger.info(f"Logging in with email: {email}")
        self.open()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    # ── Getters ──────────────────────────────────────────────────────────────

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)

    def is_login_successful(self) -> bool:
        return self.is_visible(self.WELCOME_HEADER)
