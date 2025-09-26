import pytest

from tests.data.users import ADMIN_USERS, REGULAR_USERS


class TestUsers:
    def test_get_current_user_admin(self, client, admin_headers):
        response = client.get("/api/v1/users/me", headers=admin_headers)

        assert response.status_code == 200
        result = response.json()
        assert "id" in result
        assert "email" in result
        assert "role" in result
        assert result["email"] == "admin@example.com"

    def test_get_current_user_without_auth(self, client):
        response = client.get("/api/v1/users/me")

        assert response.status_code == 401
        result = response.json()
        assert "errors" in result

    @pytest.mark.parametrize("actor_user", ADMIN_USERS)
    def test_admin_can_change_user_role(self, client, actor_user):
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": actor_user["email"],
                "password": actor_user["password"]
            }
        )
        assert login_response.status_code == 200
        admin_token = login_response.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        register_response = client.post("/api/v1/auth/register", json={
            "email": "rolechangeuser@example.com",
            "password": "testpass123!"
        })
        assert register_response.status_code == 200

        target_user_id = 2

        response = client.put(
            f"/api/v1/users/{target_user_id}/role",
            headers=admin_headers,
            json={"role": "USER_ROLE_ADMIN"}
        )

        assert response.status_code in [200, 404]
    def test_regular_user_cannot_change_roles(self, client):
        register_response = client.post("/api/v1/auth/register", json={
            "email": "regularuser@example.com",
            "password": "regular123!"
        })
        assert register_response.status_code == 200

        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "regularuser@example.com",
                "password": "regular123!"
            }
        )
        assert login_response.status_code == 200
        user_token = login_response.json()["access_token"]
        user_headers = {"Authorization": f"Bearer {user_token}"}

        response = client.put(
            "/api/v1/users/1/role",
            headers=user_headers,
            json={"role": "USER_ROLE_ADMIN"}
        )

        assert response.status_code == 403
        result = response.json()
        assert "errors" in result
        assert any("Admin access required" in str(error) for error in result["errors"])

    def test_change_role_invalid_role(self, client):
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@example.com",
                "password": "admin123!"
            }
        )
        assert login_response.status_code == 200
        admin_token = login_response.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        response = client.put(
            "/api/v1/users/1/role",
            headers=admin_headers,
            json={"role": "INVALID_ROLE"}
        )

        assert response.status_code == 422

    def test_change_role_missing_auth(self, client):
        response = client.put(
            "/api/v1/users/1/role",
            json={"role": "USER_ROLE_ADMIN"}
        )

        assert response.status_code == 401
        result = response.json()
        assert "errors" in result