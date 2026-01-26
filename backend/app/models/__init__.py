"""
Database Models Package
Export all models for easy imports
"""

from app.models.base import BaseModel
from app.models.user import User
from app.models.fitness_profile import FitnessProfile, FitnessLevel, PreferredSchedule
from app.models.gym import Gym

from app.models.match import Match, MatchStatus
from app.models.match_preference import MatchPreference, GenderPreference

from app.models.workout_plan import WorkoutPlan, PlanStatus
from app.models.workout_session import WorkoutSession

from app.models.user_stats import UserStats

__all__ = [
    "BaseModel",
    "User",
    "FitnessProfile",
    "FitnessLevel",
    "PreferredSchedule",
    "Gym",
    "Match",
    "MatchStatus",
    "MatchPreference",
    "GenderPreference",
    "WorkoutPlan",
    "PlanStatus",
    "WorkoutSession",
    "UserStats",
]
