"""
Profile Schemas
Pydantic models for fitness profile requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FitnessProfileUpdate(BaseModel):
    """Schema for updating fitness profile."""
    fitness_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    goals: Optional[List[str]] = None
    workout_types: Optional[List[str]] = None
    preferred_schedule: Optional[str] = Field(None, pattern="^(early_morning|morning|afternoon|evening|night)$")
    preferred_days: Optional[List[str]] = None
    bio: Optional[str] = Field(None, max_length=500)
    preferred_gym_id: Optional[str] = None


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
