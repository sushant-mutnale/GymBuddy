"""
Tests for User and Profile endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_header():
    """Helper to register and login, return auth header."""
    client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123", "full_name": "Test User"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestUserEndpoints:
    """Tests for /users endpoints"""

    def test_get_current_user(self):
        """Test GET /users/me returns current user."""
        headers = get_auth_header()
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user@example.com"
        assert data["full_name"] == "Test User"

    def test_get_current_user_unauthorized(self):
        """Test GET /users/me without token fails."""
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_update_current_user(self):
        """Test PUT /users/me updates user."""
        headers = get_auth_header()
        response = client.put(
            "/users/me",
            headers=headers,
            json={"full_name": "Updated Name"},
        )
        assert response.status_code == 200
        assert response.json()["full_name"] == "Updated Name"

    def test_get_user_public_profile(self):
        """Test GET /users/{id} returns public profile."""
        headers = get_auth_header()
        # Get current user id
        me_response = client.get("/users/me", headers=headers)
        user_id = me_response.json()["id"]
        # Get public profile
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert "email" not in data  # Email should not be in public profile
        assert "full_name" in data

    def test_get_user_not_found(self):
        """Test GET /users/{id} with invalid id fails."""
        response = client.get("/users/invalid-id")
        assert response.status_code == 404


class TestProfileEndpoints:
    """Tests for /profiles endpoints"""

    def test_get_my_profile(self):
        """Test GET /profiles/me returns or creates profile."""
        headers = get_auth_header()
        response = client.get("/profiles/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["fitness_level"] == "beginner"
        assert data["goals"] == []

    def test_update_my_profile(self):
        """Test PUT /profiles/me updates profile."""
        headers = get_auth_header()
        response = client.put(
            "/profiles/me",
            headers=headers,
            json={
                "fitness_level": "intermediate",
                "goals": ["build_muscle", "lose_weight"],
                "workout_types": ["strength", "hiit"],
                "preferred_schedule": "evening",
                "bio": "Fitness enthusiast",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["fitness_level"] == "intermediate"
        assert data["goals"] == ["build_muscle", "lose_weight"]
        assert data["bio"] == "Fitness enthusiast"
