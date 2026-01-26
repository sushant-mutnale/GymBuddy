"""
Matching Service
Core logic for calculating user compatibility scores and recommendations
"""

from typing import List, Dict, Optional, Tuple
from math import radians, cos, sin, asin, sqrt
from sqlalchemy.orm import Session
from sqlalchemy import not_

from app.models import User, FitnessProfile, Match, MatchPreference, MatchStatus, Gym


class MatchingService:
    """
    Service to handle user matching logic using weighted scoring.
    """

    # Scoring Weights
    WEIGHT_GOALS = 0.3
    WEIGHT_SCHEDULE = 0.3
    WEIGHT_FITNESS_LEVEL = 0.2
    WEIGHT_LOCATION = 0.2

    # Fitness Level Numeric Map
    FITNESS_LEVEL_MAP = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
    }

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate Haversine distance between two points in km.
        """
        if None in (lat1, lon1, lat2, lon2):
            return float('inf')

        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    def calculate_goal_alignment(self, profile_a: FitnessProfile, profile_b: FitnessProfile) -> float:
        """
        Calculate score (0-1) based on shared fitness goals and workout types.
        """
        if not profile_a.goals or not profile_b.goals:
            return 0.0

        # Goals overlap
        goals_a = set(profile_a.goals)
        goals_b = set(profile_b.goals)
        shared_goals = goals_a.intersection(goals_b)
        goals_score = len(shared_goals) / max(len(goals_a.union(goals_b)), 1)

        # Workout types overlap
        types_a = set(profile_a.workout_types)
        types_b = set(profile_b.workout_types)
        
        if not types_a or not types_b:
            types_score = 0.0
        else:
            shared_types = types_a.intersection(types_b)
            types_score = len(shared_types) / max(len(types_a.union(types_b)), 1)

        return (goals_score * 0.6) + (types_score * 0.4)

    def calculate_schedule_compatibility(self, profile_a: FitnessProfile, profile_b: FitnessProfile) -> float:
        """
        Calculate score (0-1) based on preferred schedule and days.
        """
        schedule_score = 1.0 if profile_a.preferred_schedule == profile_b.preferred_schedule else 0.0
        
        # If adjacent schedules (e.g. morning vs early_morning), give partial credit
        # For simplicity, precise match is 1.0, otherwise 0.0 for now unless we define partials.
        
        days_a = set(profile_a.preferred_days)
        days_b = set(profile_b.preferred_days)
        
        if not days_a or not days_b:
            days_score = 0.0
        else:
            shared_days = days_a.intersection(days_b)
            days_score = len(shared_days) / max(len(days_a.union(days_b)), 1)
            
        return (schedule_score * 0.5) + (days_score * 0.5)

    def calculate_fitness_level_compatibility(self, profile_a: FitnessProfile, profile_b: FitnessProfile) -> float:
        """
        Calculate score (0-1) based on fitness level.
        Closer levels get higher scores.
        """
        level_a = self.FITNESS_LEVEL_MAP.get(profile_a.fitness_level, 1)
        level_b = self.FITNESS_LEVEL_MAP.get(profile_b.fitness_level, 1)
        
        diff = abs(level_a - level_b)
        
        if diff == 0:
            return 1.0
        elif diff == 1:
            return 0.5
        else:
            return 0.0

    def calculate_location_proximity(self, profile_a: FitnessProfile, profile_b: FitnessProfile) -> float:
        """
        Calculate score (0-1) based on gym location proximity.
        If same preferred gym, score 1.0.
        Otherwise based on distance (inverse decay).
        """
        if profile_a.preferred_gym_id and profile_b.preferred_gym_id:
            if profile_a.preferred_gym_id == profile_b.preferred_gym_id:
                return 1.0
        
        # If no gym selected or different gyms, check gym coordinates if available
        # Need access to Gym objects, but here we only have profiles.
        # Assuming profiles have relationships loaded, or we fetch them.
        
        lat1, lon1 = None, None
        lat2, lon2 = None, None

        if profile_a.preferred_gym:
            lat1, lon1 = profile_a.preferred_gym.latitude, profile_a.preferred_gym.longitude
        if profile_b.preferred_gym:
            lat2, lon2 = profile_b.preferred_gym.latitude, profile_b.preferred_gym.longitude

        dist = self.calculate_distance(lat1, lon1, lat2, lon2)
        
        if dist == float('inf'):
            return 0.0
        
        # Score calculation: 1.0 at 0km, 0.0 at 50km
        MAX_DIST = 50.0  # km
        score = max(0.0, (MAX_DIST - dist) / MAX_DIST)
        return score

    def calculate_match_score(self, user_a: User, user_b: User) -> Dict:
        """
        Calculate comprehensive match score and breakdown.
        """
        prof_a = user_a.fitness_profile
        prof_b = user_b.fitness_profile

        if not prof_a or not prof_b:
            return {"overall_score": 0.0, "breakdown": {}}

        goal_score = self.calculate_goal_alignment(prof_a, prof_b)
        schedule_score = self.calculate_schedule_compatibility(prof_a, prof_b)
        level_score = self.calculate_fitness_level_compatibility(prof_a, prof_b)
        location_score = self.calculate_location_proximity(prof_a, prof_b)

        overall = (
            (goal_score * self.WEIGHT_GOALS) +
            (schedule_score * self.WEIGHT_SCHEDULE) +
            (level_score * self.WEIGHT_FITNESS_LEVEL) +
            (location_score * self.WEIGHT_LOCATION)
        )

        return {
            "overall_score": round(overall * 100, 1),  # 0-100 scale
            "breakdown": {
                "goals": round(goal_score * 100, 1),
                "schedule": round(schedule_score * 100, 1),
                "level": round(level_score * 100, 1),
                "location": round(location_score * 100, 1),
            }
        }

    def get_match_recommendations(self, db: Session, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Get compatible match recommendations for a user.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.fitness_profile:
            return []

        # Get user preferences
        prefs = user.match_preference
        
        # Query potential matches (exclude self)
        # In a real app, use geospatial query or more efficient filtering
        potential_users = db.query(User).filter(
            User.id != user_id,
            User.is_active == True,
        ).join(FitnessProfile).all()

        recommendations = []

        for candidate in potential_users:
            if not candidate.fitness_profile:
                continue

            # Filtering based on preferences
            if prefs:
                # Gender filter
                if prefs.gender_preference != "any" and candidate.fitness_profile.gender:
                    if candidate.fitness_profile.gender != prefs.gender_preference:
                        continue
                
                # Age filter
                if candidate.fitness_profile.age:
                     if not (prefs.min_age <= candidate.fitness_profile.age <= prefs.max_age):
                         continue
            
            # TODO: Distance filtering (basic implementation above in location score, but strictly filtering here?)
            # Leaving strict distance filter for later or SQL level.

            score_data = self.calculate_match_score(user, candidate)
            
            # Threshold for recommendation
            if score_data["overall_score"] > 20:  # arbitrary threshold
                recommendations.append({
                    "user": candidate,
                    "score": score_data["overall_score"],
                    "breakdown": score_data["breakdown"]
                })

        # Sort by score descending
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations[:limit]
