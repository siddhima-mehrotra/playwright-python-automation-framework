"""
api_client.py — Reusable API request wrapper
Wraps Playwright's APIRequestContext with logging and response validation.
"""

import json
from playwright.sync_api import APIRequestContext
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    def get(self, endpoint: str, params: dict = None) -> dict:
        logger.info(f"GET {endpoint} | params={params}")
        response = self.request.get(endpoint, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, payload: dict = None) -> dict:
        logger.info(f"POST {endpoint} | body={payload}")
        response = self.request.post(endpoint, data=json.dumps(payload))
        return self._handle_response(response)

    def put(self, endpoint: str, payload: dict = None) -> dict:
        logger.info(f"PUT {endpoint} | body={payload}")
        response = self.request.put(endpoint, data=json.dumps(payload))
        return self._handle_response(response)

    def delete(self, endpoint: str) -> int:
        logger.info(f"DELETE {endpoint}")
        response = self.request.delete(endpoint)
        logger.info(f"Response status: {response.status}")
        return response.status

    def _handle_response(self, response) -> dict:
        logger.info(f"Response status: {response.status}")
        try:
            body = response.json()
            logger.debug(f"Response body: {json.dumps(body, indent=2)}")
        except Exception:
            body = {"raw": response.text()}
        return {
            "status": response.status,
            "body": body,
            "headers": dict(response.headers),
        }
