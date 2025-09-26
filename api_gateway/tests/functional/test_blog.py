import pytest


class TestBlogPublic:

    def test_get_categories_empty(self, client):
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_get_posts_empty(self, client):
        response = client.get("/api/v1/posts")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_get_posts_by_nonexistent_category(self, client):
        response = client.get("/api/v1/categories/nonexistent/posts")
        assert response.status_code == 404

    def test_get_nonexistent_post(self, client):
        response = client.get("/api/v1/posts/nonexistent")
        assert response.status_code == 404


class TestBlogAdmin:
 
    def test_create_category_as_admin(self, client):
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

        category_data = {
            "title": "Test Category",
            "slug": "test-category",
            "description": "A test category"
        }

        response = client.post(
            "/api/v1/categories",
            headers=admin_headers,
            json=category_data
        )

        assert response.status_code == 200
        result = response.json()
        assert result["title"] == category_data["title"]
        assert result["slug"] == category_data["slug"]
        assert result["description"] == category_data["description"]
        assert "id" in result

    def test_create_category_as_user_forbidden(self, client):
        register_response = client.post("/api/v1/auth/register", json={
            "email": "testuser@example.com",
            "password": "testpass123!"
        })
        assert register_response.status_code == 200

        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser@example.com",
                "password": "testpass123!"
            }
        )
        assert login_response.status_code == 200
        user_token = login_response.json()["access_token"]
        user_headers = {"Authorization": f"Bearer {user_token}"}

        category_data = {
            "title": "Unauthorized Category",
            "slug": "unauthorized-category",
            "description": "Should not be created"
        }

        response = client.post(
            "/api/v1/categories",
            headers=user_headers,
            json=category_data
        )

        assert response.status_code == 403
        result = response.json()
        assert "errors" in result

    def test_create_post_as_admin(self, client):
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

        category_data = {
            "title": "Tech Category",
            "slug": "tech-category",
            "description": "Technology posts"
        }

        cat_response = client.post(
            "/api/v1/categories",
            headers=admin_headers,
            json=category_data
        )
        assert cat_response.status_code == 200
        category_id = cat_response.json()["id"]

        post_data = {
            "title": "Test Post",
            "slug": "test-post",
            "content_html": "<p>This is a test post with <strong>HTML</strong> content</p>",
            "category_id": category_id
        }

        response = client.post(
            "/api/v1/posts",
            headers=admin_headers,
            json=post_data
        )

        assert response.status_code == 200
        result = response.json()
        assert result["title"] == post_data["title"]
        assert result["slug"] == post_data["slug"]
        assert result["categoryId"] == category_id
        assert "id" in result
        assert "<p>" in result["contentHtml"]
        assert "<strong>" in result["contentHtml"]

    def test_create_post_with_malicious_html(self, client):
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

        category_data = {
            "title": "Security Category",
            "slug": "security-category",
            "description": "Security test posts"
        }

        cat_response = client.post(
            "/api/v1/categories",
            headers=admin_headers,
            json=category_data
        )
        assert cat_response.status_code == 200
        category_id = cat_response.json()["id"]

        post_data = {
            "title": "Security Test Post",
            "slug": "security-test-post",
            "content_html": '<p>Safe content</p><script>alert("XSS")</script><iframe src="evil.com"></iframe>',
            "category_id": category_id
        }

        response = client.post(
            "/api/v1/posts",
            headers=admin_headers,
            json=post_data
        )

        assert response.status_code == 200
        result = response.json()
        assert "<p>Safe content</p>" in result["contentHtml"]
        assert "<script>" not in result["contentHtml"]
        assert "<iframe>" not in result["contentHtml"]

    def test_create_category_without_auth(self, client):
        category_data = {
            "title": "Unauthorized Category",
            "slug": "unauthorized-category",
            "description": "Should not be created"
        }

        response = client.post("/api/v1/categories", json=category_data)
        assert response.status_code == 401

    def test_create_post_without_auth(self, client):
        post_data = {
            "title": "Unauthorized Post",
            "slug": "unauthorized-post",
            "content_html": "<p>Should not be created</p>",
            "category_id": 1
        }

        response = client.post("/api/v1/posts", json=post_data)
        assert response.status_code == 401

    def test_update_category_as_admin(self, client):
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

        category_data = {
            "title": "Original Category",
            "slug": "original-category",
            "description": "Original description"
        }

        create_response = client.post(
            "/api/v1/categories",
            headers=admin_headers,
            json=category_data
        )
        assert create_response.status_code == 200
        category_id = create_response.json()["id"]

        update_data = {
            "title": "Updated Category",
            "description": "Updated description"
        }

        response = client.put(
            f"/api/v1/categories/{category_id}",
            headers=admin_headers,
            json=update_data
        )

        assert response.status_code == 200
        result = response.json()
        assert result["title"] == update_data["title"]
        assert result["description"] == update_data["description"]

    def test_delete_category_as_admin(self, client):
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

        category_data = {
            "title": "To Be Deleted",
            "slug": "to-be-deleted",
            "description": "This will be deleted"
        }

        create_response = client.post(
            "/api/v1/categories",
            headers=admin_headers,
            json=category_data
        )
        assert create_response.status_code == 200
        category_id = create_response.json()["id"]

        response = client.delete(
            f"/api/v1/categories/{category_id}",
            headers=admin_headers
        )

        assert response.status_code == 200

        get_response = client.get("/api/v1/categories")
        assert get_response.status_code == 200
        categories = get_response.json()
        category_ids = [cat["id"] for cat in categories]
        assert category_id not in category_ids