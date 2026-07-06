"""
test_users_api.py — REST API Test Scenarios (Users endpoint)
Uses the public ReqRes API (reqres.in) — no authentication required.
Validates: status codes, response schema, payload content, and CRUD operations.
"""

import pytest
from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.api
@pytest.mark.smoke
class TestUsersAPI:

    @pytest.fixture(autouse=True)
    def setup(self, api_request_context):
        self.client = APIClient(api_request_context)

    # ── GET Tests ────────────────────────────────────────────────────────────

    def test_get_users_list_status_200(self):
        """TC-API-001 — GET /users returns 200 OK."""
        logger.info("TC-API-001: GET all users")
        response = self.client.get("/api/users", params={"page": 1})
        assert response["status"] == 200, \
            f"Expected 200, got {response['status']}"

    def test_get_users_response_schema(self):
        """TC-API-002 — Response body contains required fields."""
        logger.info("TC-API-002: Validate response schema")
        response = self.client.get("/api/users", params={"page": 1})
        body = response["body"]
        assert "data" in body, "Missing 'data' field in response"
        assert "page" in body, "Missing 'page' field in response"
        assert "total" in body, "Missing 'total' field in response"
        assert isinstance(body["data"], list), "'data' should be a list"

    def test_get_users_data_fields(self):
        """TC-API-003 — Each user object has required fields."""
        logger.info("TC-API-003: Validate user object fields")
        response = self.client.get("/api/users", params={"page": 1})
        users = response["body"]["data"]
        assert len(users) > 0, "Expected at least one user in response"
        for user in users:
            assert "id" in user, "Missing 'id' in user object"
            assert "email" in user, "Missing 'email' in user object"
            assert "first_name" in user, "Missing 'first_name' in user object"
            assert "last_name" in user, "Missing 'last_name' in user object"

    def test_get_single_user_status_200(self):
        """TC-API-004 — GET /users/{id} returns 200 for valid user."""
        logger.info("TC-API-004: GET single user by ID")
        response = self.client.get("/api/users/2")
        assert response["status"] == 200

    def test_get_single_user_correct_id(self):
        """TC-API-005 — Response contains the requested user ID."""
        logger.info("TC-API-005: Validate user ID in response")
        response = self.client.get("/api/users/2")
        assert response["body"]["data"]["id"] == 2

    def test_get_nonexistent_user_returns_404(self):
        """TC-API-006 — GET /users/{invalid_id} returns 404."""
        logger.info("TC-API-006: GET non-existent user")
        response = self.client.get("/api/users/9999")
        assert response["status"] == 404, \
            f"Expected 404 for invalid user, got {response['status']}"

    # ── POST Tests ───────────────────────────────────────────────────────────

    def test_create_user_status_201(self):
        """TC-API-007 — POST /users returns 201 Created."""
        logger.info("TC-API-007: Create new user")
        payload = {"name": "Siddhima", "job": "QA Automation Engineer"}
        response = self.client.post("/api/users", payload)
        assert response["status"] == 201, \
            f"Expected 201, got {response['status']}"

    def test_create_user_response_contains_id(self):
        """TC-API-008 — Created user response contains a generated ID."""
        logger.info("TC-API-008: Validate ID in create response")
        payload = {"name": "Test User", "job": "QA Engineer"}
        response = self.client.post("/api/users", payload)
        assert "id" in response["body"], "Expected 'id' in response body"
        assert response["body"]["id"] is not None

    def test_create_user_response_contains_name(self):
        """TC-API-009 — Created user response reflects sent name."""
        logger.info("TC-API-009: Validate name in create response")
        payload = {"name": "Automation Tester", "job": "SDET"}
        response = self.client.post("/api/users", payload)
        assert response["body"]["name"] == payload["name"]

    # ── PUT Tests ────────────────────────────────────────────────────────────

    def test_update_user_status_200(self):
        """TC-API-010 — PUT /users/{id} returns 200."""
        logger.info("TC-API-010: Update user via PUT")
        payload = {"name": "Updated Name", "job": "Senior QA Engineer"}
        response = self.client.put("/api/users/2", payload)
        assert response["status"] == 200

    def test_update_user_response_reflects_changes(self):
        """TC-API-011 — PUT response body reflects updated values."""
        logger.info("TC-API-011: Validate PUT response body")
        payload = {"name": "Siddhima M", "job": "QA Lead"}
        response = self.client.put("/api/users/2", payload)
        assert response["body"]["name"] == payload["name"]
        assert response["body"]["job"] == payload["job"]

    # ── DELETE Tests ─────────────────────────────────────────────────────────

    def test_delete_user_status_204(self):
        """TC-API-012 — DELETE /users/{id} returns 204 No Content."""
        logger.info("TC-API-012: Delete user")
        status = self.client.delete("/api/users/2")
        assert status == 204, f"Expected 204, got {status}"

    # ── Pagination Tests ─────────────────────────────────────────────────────

    @pytest.mark.parametrize("page_num,expected_page", [
        (1, 1),
        (2, 2),
    ])
    def test_pagination(self, page_num, expected_page):
        """TC-API-013 — Pagination returns correct page number."""
        logger.info(f"TC-API-013: Testing pagination — page {page_num}")
        response = self.client.get("/api/users", params={"page": page_num})
        assert response["body"]["page"] == expected_page
