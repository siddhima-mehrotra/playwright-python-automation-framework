"""
test_login.py — UI Login Test Scenarios
Tests login functionality using Page Object Model.
"""

import pytest
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
@pytest.mark.ui
class TestLogin:

    def test_valid_login(self, page, test_credentials):
        """TC001 — Valid credentials should redirect to dashboard."""
        logger.info("TC001: Testing valid login")
        login_page = LoginPage(page)
        login_page.login(
            email=test_credentials["email"],
            password=test_credentials["password"]
        )
        assert login_page.is_login_successful(), \
            "Expected to land on dashboard after valid login"

    def test_invalid_password(self, page):
        """TC002 — Invalid password should show error message."""
        logger.info("TC002: Testing invalid password")
        login_page = LoginPage(page)
        login_page.login(email="valid@example.com", password="wrongpassword")
        assert login_page.is_error_displayed(), \
            "Expected error message for invalid password"

    def test_empty_email(self, page):
        """TC003 — Empty email should show validation error."""
        logger.info("TC003: Testing empty email field")
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_password("somepassword")
        login_page.click_login()
        assert login_page.is_error_displayed(), \
            "Expected validation error for empty email"

    def test_empty_password(self, page):
        """TC004 — Empty password should show validation error."""
        logger.info("TC004: Testing empty password field")
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_email("user@example.com")
        login_page.click_login()
        assert login_page.is_error_displayed(), \
            "Expected validation error for empty password"

    @pytest.mark.parametrize("email,password", [
        ("notanemail", "pass123"),
        ("@domain.com", "pass123"),
        ("user@", "pass123"),
    ])
    def test_invalid_email_formats(self, page, email, password):
        """TC005 — Various invalid email formats should be rejected."""
        logger.info(f"TC005: Testing invalid email format: {email}")
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login()
        assert login_page.is_error_displayed(), \
            f"Expected error for invalid email format: {email}"
