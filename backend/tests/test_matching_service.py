"""
Tests for Matching Service
"""

import pytest
from app.services.matching_service import MatchingService
from app.models import User, FitnessProfile, MatchPreference, Gym, FitnessLevel

class TestMatchingServiceLogic:
    """Unit tests for scoring logic"""

    def test_calculate_goal_alignment(self):
        service = MatchingService()
        
        # Perfect match
        p1 = FitnessProfile(goals=["muscle"], workout_types=["strength"])
        p2 = FitnessProfile(goals=["muscle"], workout_types=["strength"])
        assert service.calculate_goal_alignment(p1, p2) == 1.0
        
        # Partial match
        p3 = FitnessProfile(goals=["muscle", "cardio"], workout_types=["strength"])
        p4 = FitnessProfile(goals=["muscle"], workout_types=["yoga"])
        # Goals: 1/2 = 0.5 * 0.6 = 0.3
        # Types: 0/2 = 0.0 * 0.4 = 0.0
        # Total: 0.3
        assert service.calculate_goal_alignment(p3, p4) == 0.3
        
        # No match
        p5 = FitnessProfile(goals=["muscle"], workout_types=["strength"])
        p6 = FitnessProfile(goals=["cardio"], workout_types=["yoga"])
        assert service.calculate_goal_alignment(p5, p6) == 0.0

    def test_calculate_schedule_compatibility(self):
        service = MatchingService()
        
        # Exact schedule
        p1 = FitnessProfile(preferred_schedule="morning", preferred_days=["mon"])
        p2 = FitnessProfile(preferred_schedule="morning", preferred_days=["mon"])
        assert service.calculate_schedule_compatibility(p1, p2) == 1.0
        
        # Different schedule, same days
        p3 = FitnessProfile(preferred_schedule="morning", preferred_days=["mon", "tue"])
        p4 = FitnessProfile(preferred_schedule="evening", preferred_days=["mon"])
        # Schedule: 0 * 0.5 = 0
        # Days: 1/2 = 0.5 * 0.5 = 0.25
        # Total: 0.25
        assert service.calculate_schedule_compatibility(p3, p4) == 0.25

    def test_calculate_fitness_level_compatibility(self):
        service = MatchingService()
        
        # Same level
        p1 = FitnessProfile(fitness_level="beginner")
        p2 = FitnessProfile(fitness_level="beginner")
        assert service.calculate_fitness_level_compatibility(p1, p2) == 1.0
        
        # Adjacent level
        p3 = FitnessProfile(fitness_level="beginner")
        p4 = FitnessProfile(fitness_level="intermediate")
        assert service.calculate_fitness_level_compatibility(p3, p4) == 0.5
        
        # Far level
        p5 = FitnessProfile(fitness_level="beginner")
        p6 = FitnessProfile(fitness_level="advanced")
        assert service.calculate_fitness_level_compatibility(p5, p6) == 0.0

    def test_calculate_location_proximity(self):
        service = MatchingService()
        
        # Same gym
        p1 = FitnessProfile(preferred_gym_id="gym1")
        p2 = FitnessProfile(preferred_gym_id="gym1")
        assert service.calculate_location_proximity(p1, p2) == 1.0
        
        # Different gyms with coordinates
        # Gym 1: (10, 10)
        # Gym 2: (10, 10.1) -> ~11km distance usually
        g1 = Gym(latitude=10.0, longitude=10.0)
        g2 = Gym(latitude=10.0, longitude=10.1)
        p3 = FitnessProfile(preferred_gym=g1)
        p4 = FitnessProfile(preferred_gym=g2)
        
        score = service.calculate_location_proximity(p3, p4)
        assert 0.0 < score < 1.0
        
        # Too far
        g3 = Gym(latitude=10.0, longitude=10.0)
        g4 = Gym(latitude=20.0, longitude=20.0) # Very far
        p5 = FitnessProfile(preferred_gym=g3)
        p6 = FitnessProfile(preferred_gym=g4)
        assert service.calculate_location_proximity(p5, p6) == 0.0


class TestMatchingServiceIntegration:
    """Integration tests with database"""
    
    def test_get_match_recommendations(self, db_session):
        service = MatchingService()
        
        # Create user A
        user_a = User(email="a@test.com", hashed_password="pw", is_active=True, is_verified=True)
        prof_a = FitnessProfile(
            user=user_a,
            fitness_level="beginner",
            goals=["muscle"],
            workout_types=["strength"],
            preferred_schedule="morning",
            preferred_days=["mon", "wed", "fri"],
            gender="male"
        )
        pref_a = MatchPreference(user=user_a, gender_preference="female")
        db_session.add(user_a)
        
        # Create user B (Compatible)
        user_b = User(email="b@test.com", hashed_password="pw", is_active=True, is_verified=True)
        prof_b = FitnessProfile(
            user=user_b,
            fitness_level="beginner",
            goals=["muscle"],
            workout_types=["strength"],
            preferred_schedule="morning",
            preferred_days=["mon", "wed", "fri"],
            gender="female"
        )
        db_session.add(user_b)
        
        # Create user C (Incompatible Gender)
        user_c = User(email="c@test.com", hashed_password="pw", is_active=True, is_verified=True)
        prof_c = FitnessProfile(
            user=user_c,
            fitness_level="beginner",
            goals=["muscle"],
            workout_types=["strength"],
            preferred_schedule="morning",
            gender="male"
        )
        db_session.add(user_c)
        
        db_session.commit()
        db_session.refresh(user_a)
        
        # Get recommendations
        recommendations = service.get_match_recommendations(db_session, user_a.id)
        
        # User B should be recommended (high score, gender match)
        # User C should be filtered out (gender mismatch)
        
        assert len(recommendations) == 1
        assert recommendations[0]["user"].id == user_b.id
        assert recommendations[0]["score"] == 80.0
