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
]
