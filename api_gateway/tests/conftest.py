import os
import pytest
from starlette.testclient import TestClient

from tests.data.users import TEST_USERS, ADMIN_USERS, REGULAR_USERS

os.environ["APP_ENV"] = "TESTING"


@pytest.fixture
def client():
    """FastAPI test client"""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def admin_user():
    """Admin user for testing admin functionality"""
    return ADMIN_USERS[0]


@pytest.fixture
def regular_user():
    """Regular user for testing user functionality"""
    return REGULAR_USERS[0]


@pytest.fixture
def auth_token(client, actor_user):
    """Get JWT token for a user"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": actor_user["email"],
            "password": actor_user["password"]
        }
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def auth_headers(auth_token):
    """Authorization headers with Bearer token"""
    return {"Authorization": f"Bearer {auth_token['access_token']}"}


@pytest.fixture
def admin_token(client, admin_user):
    """Get JWT token for admin user"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": admin_user["email"],
            "password": admin_user["password"]
        }
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def admin_headers(admin_token):
    """Authorization headers for admin user"""
    return {"Authorization": f"Bearer {admin_token['access_token']}"}


@pytest.fixture
def user_token(client, regular_user):
    """Get JWT token for regular user"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": regular_user["email"],
            "password": regular_user["password"]
        }
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def user_headers(user_token):
    """Authorization headers for regular user"""
    return {"Authorization": f"Bearer {user_token['access_token']}"}


