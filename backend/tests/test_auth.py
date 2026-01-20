"""
Tests for Auth endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


class TestRegister:
    """Tests for POST /auth/register"""

    def test_register_success(self):
        """Test successful user registration."""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "full_name": "Test User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert data["is_active"] is True
        assert "id" in data

    def test_register_duplicate_email(self):
        """Test registration with existing email fails."""
        # Register first user
        client.post(
            "/auth/register",
            json={"email": "duplicate@example.com", "password": "password123"},
        )
        # Try to register with same email
        response = client.post(
            "/auth/register",
            json={"email": "duplicate@example.com", "password": "different123"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_register_short_password(self):
        """Test registration with short password fails."""
        response = client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "short"},
        )
        assert response.status_code == 422  # Validation error


class TestLogin:
    """Tests for POST /auth/login"""

    def test_login_success(self):
        """Test successful login returns tokens."""
        # Register user first
        client.post(
            "/auth/register",
            json={"email": "login@example.com", "password": "password123"},
        )
        # Login
        response = client.post(
            "/auth/login",
            json={"email": "login@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_email(self):
        """Test login with non-existent email fails."""
        response = client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

    def test_login_invalid_password(self):
        """Test login with wrong password fails."""
        # Register user first
        client.post(
            "/auth/register",
            json={"email": "wrongpass@example.com", "password": "password123"},
        )
        # Login with wrong password
        response = client.post(
            "/auth/login",
            json={"email": "wrongpass@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"


class TestRefresh:
    """Tests for POST /auth/refresh"""

    def test_refresh_success(self):
        """Test successful token refresh."""
        # Register and login
        client.post(
            "/auth/register",
            json={"email": "refresh@example.com", "password": "password123"},
        )
        login_response = client.post(
            "/auth/login",
            json={"email": "refresh@example.com", "password": "password123"},
        )
        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_refresh_invalid_token(self):
        """Test refresh with invalid token fails."""
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": "invalid_token"},
        )
        assert response.status_code == 401
