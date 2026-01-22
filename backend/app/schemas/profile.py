"""
Profile Schemas
Pydantic models for fitness profile requests and responses
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum


class FitnessLevel(str, Enum):
    """Fitness level enum."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class PreferredSchedule(str, Enum):
    """Preferred workout schedule enum."""
    EARLY_MORNING = "early_morning"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class WorkoutDay(str, Enum):
    """Days of the week enum."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class WorkoutType(str, Enum):
    """Workout type enum."""
    STRENGTH = "strength"
    CARDIO = "cardio"
    HIIT = "hiit"
    YOGA = "yoga"
    CROSSFIT = "crossfit"
    POWERLIFTING = "powerlifting"
    BODYBUILDING = "bodybuilding"
    FUNCTIONAL = "functional"
    SWIMMING = "swimming"
    BOXING = "boxing"


class FitnessGoal(str, Enum):
    """Fitness goal enum."""
    BUILD_MUSCLE = "build_muscle"
    LOSE_WEIGHT = "lose_weight"
    INCREASE_STRENGTH = "increase_strength"
    IMPROVE_CARDIO = "improve_cardio"
    STAY_FIT = "stay_fit"
    FLEXIBILITY = "flexibility"


class FitnessProfileUpdate(BaseModel):
    """Schema for updating fitness profile."""
    fitness_level: Optional[FitnessLevel] = None
    goals: Optional[List[FitnessGoal]] = None
    workout_types: Optional[List[WorkoutType]] = None
    preferred_schedule: Optional[PreferredSchedule] = None
    preferred_days: Optional[List[WorkoutDay]] = None
    bio: Optional[str] = Field(None, max_length=500)
    preferred_gym_id: Optional[str] = None

    @field_validator('goals')
    @classmethod
    def validate_goals(cls, v):
        if v and len(v) > 5:
            raise ValueError('Maximum 5 goals allowed')
        return v

    @field_validator('workout_types')
    @classmethod
    def validate_workout_types(cls, v):
        if v and len(v) > 6:
            raise ValueError('Maximum 6 workout types allowed')
        return v


class FitnessProfileResponse(BaseModel):
    """Schema for fitness profile response."""
    id: str
    user_id: str
    fitness_level: str
    goals: List[str]
    workout_types: List[str]
    preferred_schedule: str
    preferred_days: List[str]
    bio: Optional[str] = None
    preferred_gym_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
