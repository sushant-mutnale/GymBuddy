"""
Tests for Workout endpoints
"""

import pytest
from fastapi.testclient import TestClient
from datetime import date
from app.main import app

client = TestClient(app)


def create_user_with_profile(email: str = "workout_user@test.com"):
    """Helper to create a user with profile."""
    client.post("/auth/register", json={
        "email": email,
        "password": "password123",
        "full_name": "Workout User"
    })
    login_resp = client.post("/auth/login", json={
        "email": email,
        "password": "password123"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Update fitness profile
    client.put("/profiles/me", headers=headers, json={
        "fitness_level": "intermediate",
        "goals": ["build_muscle"],
        "workout_types": ["strength"],
        "preferred_schedule": "morning",
        "preferred_days": ["monday", "wednesday", "friday"],
    })
    
    return headers


class TestWorkoutPlans:
    """Tests for workout plan endpoints"""

    def test_generate_plan(self, db_session):
        """Test generating a workout plan."""
        headers = create_user_with_profile("plan_gen@test.com")
        
        response = client.post("/workouts/plans/generate", headers=headers, json={"weeks": 4})
        assert response.status_code == 201
        data = response.json()
        
        assert "id" in data
        assert data["name"] == "Intermediate Push-Pull-Legs"
        assert data["target_goal"] == "build_muscle"
        assert "days" in data["plan_data"]
        assert len(data["plan_data"]["days"]) >= 3

    def test_list_plans(self, db_session):
        """Test listing workout plans."""
        headers = create_user_with_profile("list_plans@test.com")
        
        # Generate a plan first
        client.post("/workouts/plans/generate", headers=headers)
        
        response = client.get("/workouts/plans", headers=headers)
        assert response.status_code == 200
        plans = response.json()
        assert len(plans) >= 1
        assert plans[0]["status"] == "active"


class TestWorkoutSessions:
    """Tests for workout session endpoints"""

    def test_log_session(self, db_session):
        """Test logging a workout session."""
        headers = create_user_with_profile("log_session@test.com")
        
        response = client.post("/workouts/sessions", headers=headers, json={
            "date": str(date.today()),
            "duration_minutes": 60,
            "calories_burned": 500,
            "exercises_completed": 8,
            "energy_level": 4,
            "mood_after": 5,
            "notes": "Great workout!"
        })
        assert response.status_code == 201
        data = response.json()
        
        assert data["duration_minutes"] == 60
        assert data["calories_burned"] == 500
        assert data["mood_after"] == 5

    def test_list_sessions(self, db_session):
        """Test listing workout sessions."""
        headers = create_user_with_profile("list_sessions@test.com")
        
        # Log a session first
        client.post("/workouts/sessions", headers=headers, json={
            "date": str(date.today()),
            "duration_minutes": 45
        })
        
        response = client.get("/workouts/sessions", headers=headers)
        assert response.status_code == 200
        sessions = response.json()
        assert len(sessions) >= 1

    def test_session_linked_to_plan(self, db_session):
        """Test that session can be linked to a plan."""
        headers = create_user_with_profile("linked_session@test.com")
        
        # Generate a plan
        plan_resp = client.post("/workouts/plans/generate", headers=headers)
        plan_id = plan_resp.json()["id"]
        
        # Log session with plan_id
        session_resp = client.post("/workouts/sessions", headers=headers, json={
            "date": str(date.today()),
            "duration_minutes": 50,
            "plan_id": plan_id
        })
        assert session_resp.status_code == 201
        assert session_resp.json()["plan_id"] == plan_id
