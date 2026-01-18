"""
Database Models Package
Export all models for easy imports
"""

from app.models.base import BaseModel
from app.models.user import User
from app.models.fitness_profile import FitnessProfile, FitnessLevel, PreferredSchedule
from app.models.gym import Gym

__all__ = [
    "BaseModel",
    "User",
    "FitnessProfile",
    "FitnessLevel",
    "PreferredSchedule",
    "Gym",
]
