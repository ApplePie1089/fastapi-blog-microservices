import pytest
from copy import copy

from tests.data.users import REGULAR_USERS, ADMIN_USERS


class TestAuth:
    @pytest.mark.dependency(name="register", scope="session")
    def test_register_new_user(self, client):
        new_user = {
            "email": "newuser@test.com",
            "password": "newuser123!"
        }

        response = client.post("/api/v1/auth/register", json=new_user)
        assert response.status_code == 200

        result = response.json()
        assert "access_token" in result
        assert "token_type" in result
        assert "expires_in" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"

    def test_register_existing_user(self, client):
        existing_user = {
            "email": "admin@example.com",
            "password": "admin123!"
        }

        response = client.post("/api/v1/auth/register", json=existing_user)
        assert response.status_code in [500]

    def test_register_invalid_email(self, client):
        invalid_user = {
            "email": "invalid-email",
            "password": "password123!"
        }

        response = client.post("/api/v1/auth/register", json=invalid_user)
        assert response.status_code == 422

    def test_login_admin(self, client):
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@example.com",
                "password": "admin123!"
            }
        )

        assert response.status_code == 200
        result = response.json()
        assert "access_token" in result
        assert "token_type" in result
        assert "expires_in" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@example.com",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        result = response.json()
        assert "errors" in result

    def test_login_wrong_email(self, client):
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "password123"
            }
        )

        assert response.status_code == 401
        result = response.json()
        assert "errors" in result

    def test_refresh_token(self, client):
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@example.com",
                "password": "admin123!"
            }
        )

        assert login_response.status_code == 200
        login_data = login_response.json()
        refresh_token = login_data["refresh_token"]

        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        result = response.json()
        assert "access_token" in result
        assert "token_type" in result
        assert "expires_in" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"

    def test_refresh_invalid_token(self, client):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token_here"}
        )

        assert response.status_code == 401
        result = response.json()
        assert "errors" in result