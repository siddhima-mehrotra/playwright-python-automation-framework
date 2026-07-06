"""
conftest.py — Global fixtures, hooks, and browser setup
Applies to all tests in the framework
"""

import os
import pytest
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


# ── Browser & Page Fixtures ─────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    """Launch browser once per test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        logger.info("Browser launched: Chromium (headless)")
        yield browser
        browser.close()
        logger.info("Browser closed.")


@pytest.fixture(scope="function")
def context(browser_instance: Browser):
    """Create a fresh browser context for each test."""
    ctx = browser_instance.new_context(
        base_url=os.getenv("BASE_URL", "https://reqres.in"),
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
        record_video_dir="reports/videos/" if os.getenv("RECORD_VIDEO") else None,
    )
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Open a new page for each test."""
    pg = context.new_page()
    yield pg
    pg.close()


@pytest.fixture(scope="session")
def api_request_context():
    """Shared API request context for API tests."""
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=os.getenv("API_BASE_URL", "https://reqres.in"),
            extra_http_headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        logger.info("API request context created.")
        yield request_context
        request_context.dispose()


# ── Environment Fixtures ─────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://reqres.in")


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", "https://reqres.in/api")


@pytest.fixture(scope="session")
def test_credentials():
    return {
        "email": os.getenv("TEST_EMAIL", "eve.holt@reqres.in"),
        "password": os.getenv("TEST_PASSWORD", "cityslicka"),
    }


# ── Hooks ────────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take a screenshot on test failure."""
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        page = item.funcargs.get("page")
        if page:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("/", "_").replace(" ", "_")
            screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
            os.makedirs("reports/screenshots", exist_ok=True)
            page.screenshot(path=screenshot_path, full_page=True)
            logger.error(f"Test FAILED — screenshot saved: {screenshot_path}")


def pytest_configure(config):
    """Create report directories before tests run."""
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/videos", exist_ok=True)
    logger.info("Test session starting — report directories ready.")


def pytest_sessionfinish(session, exitstatus):
    """Log session completion."""
    total = session.testscollected
    logger.info(f"Test session complete. Total tests: {total} | Exit status: {exitstatus}")
