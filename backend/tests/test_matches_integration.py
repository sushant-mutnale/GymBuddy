"""
Integration Tests for Matching API
End-to-end tests for the matching workflow
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_user_with_profile(email: str, password: str, name: str, gender: str, goals: list, schedule: str):
    """Helper to create a user with profile."""
    # Register
    client.post("/auth/register", json={"email": email, "password": password, "full_name": name})
    
    # Login
    login_resp = client.post("/auth/login", json={"email": email, "password": password})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update fitness profile
    client.put("/profiles/me", headers=headers, json={
        "fitness_level": "intermediate",
        "goals": goals,
        "workout_types": ["strength", "cardio"],
        "preferred_schedule": schedule,
        "preferred_days": ["monday", "wednesday", "friday"],
        "gender": gender,
        "bio": f"Test bio for {name}"
    })
    
    # Get user ID
    me_resp = client.get("/users/me", headers=headers)
    user_id = me_resp.json()["id"]
    
    return {"user_id": user_id, "headers": headers, "email": email}


class TestMatchingAPIIntegration:
    """End-to-end integration tests for matching flow."""

    def test_full_matching_flow(self, db_session):
        """Test complete flow: create users, get recommendations, send/accept match."""
        # Create 4 users with different profiles
        user_a = create_user_with_profile(
            "alice@test.com", "password123", "Alice", "female",
            ["build_muscle", "lose_weight"], "morning"
        )
        user_b = create_user_with_profile(
            "bob@test.com", "password123", "Bob", "male",
            ["build_muscle", "lose_weight"], "morning"
        )
        user_c = create_user_with_profile(
            "charlie@test.com", "password123", "Charlie", "male",
            ["improve_cardio"], "evening"
        )
        user_d = create_user_with_profile(
            "diana@test.com", "password123", "Diana", "female",
            ["build_muscle"], "morning"
        )
        
        # Alice gets recommendations
        recs_resp = client.get("/matches/recommendations", headers=user_a["headers"])
        assert recs_resp.status_code == 200
        recommendations = recs_resp.json()
        assert len(recommendations) >= 1
        
        # Alice sends match request to Bob
        request_resp = client.post(
            f"/matches/{user_b['user_id']}/request",
            headers=user_a["headers"]
        )
        assert request_resp.status_code == 201
        match_id = request_resp.json()["match_id"]
        
        # Bob sees pending match
        matches_resp = client.get("/matches?status_filter=pending", headers=user_b["headers"])
        assert matches_resp.status_code == 200
        pending = matches_resp.json()
        assert len(pending) == 1
        assert pending[0]["id"] == match_id
        
        # Bob accepts match
        accept_resp = client.post(f"/matches/{match_id}/accept", headers=user_b["headers"])
        assert accept_resp.status_code == 200
        
        # Verify match is accepted
        matches_resp = client.get("/matches?status_filter=accepted", headers=user_a["headers"])
        accepted = matches_resp.json()
        assert len(accepted) == 1
        assert accepted[0]["status"] == "accepted"

    def test_cannot_match_self(self, db_session):
        """Test that a user cannot send match request to themselves."""
        user = create_user_with_profile(
            "self@test.com", "password123", "Self", "male",
            ["build_muscle"], "morning"
        )
        
        resp = client.post(f"/matches/{user['user_id']}/request", headers=user["headers"])
        assert resp.status_code == 400
        assert "yourself" in resp.json()["detail"]

    def test_only_recipient_can_accept(self, db_session):
        """Test that only the recipient can accept/reject a match."""
        user_a = create_user_with_profile(
            "sender@test.com", "password123", "Sender", "male",
            ["build_muscle"], "morning"
        )
        user_b = create_user_with_profile(
            "receiver@test.com", "password123", "Receiver", "female",
            ["build_muscle"], "morning"
        )
        
        # A sends request to B
        resp = client.post(f"/matches/{user_b['user_id']}/request", headers=user_a["headers"])
        match_id = resp.json()["match_id"]
        
        # A tries to accept (should fail - only B can accept)
        accept_resp = client.post(f"/matches/{match_id}/accept", headers=user_a["headers"])
        assert accept_resp.status_code == 403

    def test_reject_match(self, db_session):
        """Test rejecting a match request."""
        user_a = create_user_with_profile(
            "requester@test.com", "password123", "Requester", "male",
            ["build_muscle"], "morning"
        )
        user_b = create_user_with_profile(
            "rejecter@test.com", "password123", "Rejecter", "female",
            ["build_muscle"], "morning"
        )
        
        # A sends request to B
        resp = client.post(f"/matches/{user_b['user_id']}/request", headers=user_a["headers"])
        match_id = resp.json()["match_id"]
        
        # B rejects
        reject_resp = client.post(f"/matches/{match_id}/reject", headers=user_b["headers"])
        assert reject_resp.status_code == 200
        
        # Verify status
        matches_resp = client.get("/matches", headers=user_b["headers"])
        matches = matches_resp.json()
        assert matches[0]["status"] == "rejected"
