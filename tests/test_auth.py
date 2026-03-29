# tests/test_auth.py


class TestRegister:
    """Tests for user registration"""

    def test_register_admin_success(self, client):
        """A new admin user can register successfully"""
        response = client.post("/auth/register", json={
            "email": "newadmin@test.com",
            "full_name": "New Admin",
            "password": "password123",
            "role": "admin"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newadmin@test.com"
        assert data["role"] == "admin"
        # Password must NEVER appear in response
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_staff_success(self, client):
        """A new staff user can register successfully"""
        response = client.post("/auth/register", json={
            "email": "newstaff@test.com",
            "full_name": "New Staff",
            "password": "password123",
            "role": "staff"
        })
        assert response.status_code == 201
        assert response.json()["role"] == "staff"

    def test_register_duplicate_email_fails(self, client):
        """Registering with an existing email returns 400"""
        # Register once
        client.post("/auth/register", json={
            "email": "duplicate@test.com",
            "full_name": "First User",
            "password": "password123",
            "role": "staff"
        })
        # Try to register again with same email
        response = client.post("/auth/register", json={
            "email": "duplicate@test.com",
            "full_name": "Second User",
            "password": "password456",
            "role": "staff"
        })
        assert response.status_code == 400

    def test_register_invalid_email_fails(self, client):
        """Invalid email format returns validation error"""
        response = client.post("/auth/register", json={
            "email": "not-an-email",
            "full_name": "Bad User",
            "password": "password123",
            "role": "staff"
        })
        assert response.status_code == 422

    def test_register_short_password_fails(self, client):
        """Password shorter than 6 characters is rejected"""
        response = client.post("/auth/register", json={
            "email": "user@test.com",
            "full_name": "User",
            "password": "abc",
            "role": "staff"
        })
        assert response.status_code == 422


class TestLogin:
    """Tests for user login"""

    def test_login_success(self, client):
        """Valid credentials return a JWT token"""
        # Register first
        client.post("/auth/register", json={
            "email": "loginuser@test.com",
            "full_name": "Login User",
            "password": "password123",
            "role": "staff"
        })
        # Login
        response = client.post("/auth/login", json={
            "email": "loginuser@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_wrong_password_fails(self, client):
        """Wrong password returns 401"""
        client.post("/auth/register", json={
            "email": "user@test.com",
            "full_name": "User",
            "password": "correctpassword",
            "role": "staff"
        })
        response = client.post("/auth/login", json={
            "email": "user@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user_fails(self, client):
        """Login with email that doesn't exist returns 401"""
        response = client.post("/auth/login", json={
            "email": "nobody@test.com",
            "password": "password123"
        })
        assert response.status_code == 401


class TestProtectedRoutes:
    """Tests for authentication on protected routes"""

    def test_get_my_profile_with_token(self, client, staff_headers):
        """Authenticated user can get their profile"""
        response = client.get("/auth/me", headers=staff_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "staff@test.com"

    def test_get_my_profile_without_token_fails(self, client):
        """Unauthenticated request to protected route returns 401"""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_all_users_admin_only(self, client, admin_headers, staff_headers):
        """Only admin can list all users"""
        # Admin should succeed
        admin_response = client.get("/auth/users", headers=admin_headers)
        assert admin_response.status_code == 200

        # Staff should be forbidden
        staff_response = client.get("/auth/users", headers=staff_headers)
        assert staff_response.status_code == 403