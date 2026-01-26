"""
Workouts Router
Endpoints for workout plans and sessions
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas.workout import (
    WorkoutPlanCreate,
    WorkoutPlanResponse,
    WorkoutSessionCreate,
    WorkoutSessionResponse,
)
from app.dependencies import get_current_user
from app.services.workout_service import WorkoutService

router = APIRouter(prefix="/workouts", tags=["Workouts"])
workout_service = WorkoutService()


@router.post("/plans/generate", response_model=WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
def generate_plan(
    plan_data: WorkoutPlanCreate = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a workout plan based on user's fitness profile."""
    if not current_user.fitness_profile:
        raise HTTPException(
            status_code=400,
            detail="Please complete your fitness profile first"
        )
    
    weeks = plan_data.weeks if plan_data else 4
    plan = workout_service.generate_plan(db, current_user, weeks)
    return plan


@router.get("/plans", response_model=List[WorkoutPlanResponse])
def list_plans(
    status_filter: str = Query(default=None, description="Filter by status: active, completed, cancelled"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all workout plans for the current user."""
    plans = workout_service.get_user_plans(db, current_user.id, status_filter)
    return plans


@router.post("/sessions", response_model=WorkoutSessionResponse, status_code=status.HTTP_201_CREATED)
def log_session(
    session_data: WorkoutSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a workout session."""
    session = workout_service.log_session(
        db=db,
        user_id=current_user.id,
        session_date=session_data.date,
        duration_minutes=session_data.duration_minutes,
        plan_id=session_data.plan_id,
        notes=session_data.notes,
        calories_burned=session_data.calories_burned,
        exercises_completed=session_data.exercises_completed,
        energy_level=session_data.energy_level,
        mood_after=session_data.mood_after,
    )
    return session


@router.get("/sessions", response_model=List[WorkoutSessionResponse])
def list_sessions(
    limit: int = Query(default=50, le=100),
    plan_id: str = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get workout session history."""
    sessions = workout_service.get_user_sessions(
        db, current_user.id, limit=limit, plan_id=plan_id
    )
    return sessions
