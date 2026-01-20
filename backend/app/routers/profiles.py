"""
Profile Router
Fitness profile endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, FitnessProfile
from app.schemas.profile import FitnessProfileUpdate, FitnessProfileResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/me", response_model=FitnessProfileResponse)
def get_my_fitness_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user's fitness profile."""
    profile = db.query(FitnessProfile).filter(
        FitnessProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create default profile if not exists
        profile = FitnessProfile(
            user_id=current_user.id,
            fitness_level="beginner",
            goals=[],
            workout_types=[],
            preferred_schedule="morning",
            preferred_days=[],
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile


@router.put("/me", response_model=FitnessProfileResponse)
def update_my_fitness_profile(
    profile_data: FitnessProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user's fitness profile."""
    profile = db.query(FitnessProfile).filter(
        FitnessProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        # Create profile if not exists
        profile = FitnessProfile(user_id=current_user.id)
        db.add(profile)
    
    # Update fields
    if profile_data.fitness_level is not None:
        profile.fitness_level = profile_data.fitness_level
    if profile_data.goals is not None:
        profile.goals = profile_data.goals
    if profile_data.workout_types is not None:
        profile.workout_types = profile_data.workout_types
    if profile_data.preferred_schedule is not None:
        profile.preferred_schedule = profile_data.preferred_schedule
    if profile_data.preferred_days is not None:
        profile.preferred_days = profile_data.preferred_days
    if profile_data.bio is not None:
        profile.bio = profile_data.bio
    if profile_data.preferred_gym_id is not None:
        profile.preferred_gym_id = profile_data.preferred_gym_id
    
    db.commit()
    db.refresh(profile)
    return profile
