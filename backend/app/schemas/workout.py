"""
Workout Schemas
Pydantic models for workout requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date, datetime


class WorkoutPlanCreate(BaseModel):
    """Request to generate a workout plan."""
    weeks: int = Field(default=4, ge=1, le=12)


class WorkoutPlanResponse(BaseModel):
    """Workout plan response."""
    id: str
    name: str
    description: Optional[str] = None
    plan_data: Dict
    plan_type: Optional[str] = None
    target_goal: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutSessionCreate(BaseModel):
    """Request to log a workout session."""
    date: date
    duration_minutes: Optional[int] = Field(None, ge=1, le=480)
    plan_id: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=1000)
    calories_burned: Optional[int] = Field(None, ge=0)
    exercises_completed: Optional[int] = Field(None, ge=0)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    mood_after: Optional[int] = Field(None, ge=1, le=5)


class WorkoutSessionResponse(BaseModel):
    """Workout session response."""
    id: str
    user_id: str
    plan_id: Optional[str] = None
    date: date
    duration_minutes: Optional[int] = None
    calories_burned: Optional[int] = None
    exercises_completed: Optional[int] = None
    notes: Optional[str] = None
    energy_level: Optional[int] = None
    mood_after: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
