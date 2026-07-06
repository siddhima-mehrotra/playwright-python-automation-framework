"""
retry.py — Retry decorator for flaky element interactions
Automatically retries failing actions up to max_attempts times.
"""

import time
import functools
from utils.logger import get_logger

logger = get_logger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions=(Exception,)):
    """
    Decorator that retries a function on failure.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Seconds to wait between retries
        exceptions: Exception types to catch and retry

    Usage:
        @retry(max_attempts=3, delay=1)
        def click(self, selector):
            self.page.locator(selector).click()
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for "
                        f"'{func.__name__}': {str(e)}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            logger.error(
                f"All {max_attempts} attempts failed for '{func.__name__}'. "
                f"Last error: {str(last_exception)}"
            )
            raise last_exception
        return wrapper
    return decorator
