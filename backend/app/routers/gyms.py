"""
Gyms Router
Endpoints for Gym Discovery and Check-in
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import User, Gym, FitnessProfile
from app.schemas.gym import GymCreate, GymResponse, GymRecommendationResponse
from app.dependencies import get_current_user
import math

router = APIRouter(prefix="/gyms", tags=["Gyms"])

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km"""
    if None in (lat1, lon1, lat2, lon2):
        return None
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

@router.get("", response_model=List[GymRecommendationResponse])
def search_gyms(
    query: str = Query(None, description="Search by name or city"),
    lat: float = Query(None, description="User latitude"),
    lon: float = Query(None, description="User longitude"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search for gyms, optionally sorted by distance."""
    db_query = db.query(Gym).filter(Gym.is_active == True)
    
    if query:
        search = f"%{query}%"
        db_query = db_query.filter(
            (Gym.name.ilike(search)) | (Gym.city.ilike(search))
        )
        
    gyms = db_query.limit(50).all()
    
    results = []
    for gym in gyms:
        dist = haversine(lat, lon, gym.latitude, gym.longitude) if lat and lon else None
        
        # Count members using this gym as their preference
        member_count = db.query(FitnessProfile).filter(FitnessProfile.preferred_gym_id == gym.id).count()
        
        gym_dict = gym.__dict__.copy()
        gym_dict["distance_km"] = dist
        gym_dict["member_count"] = member_count
        results.append(GymRecommendationResponse(**gym_dict))
        
    if lat and lon:
        # Sort by distance
        results.sort(key=lambda x: x.distance_km if x.distance_km is not None else float('inf'))
    else:
        # Sort by popularity
        results.sort(key=lambda x: x.member_count, reverse=True)
        
    return results

@router.post("", response_model=GymResponse, status_code=status.HTTP_201_CREATED)
def create_gym(
    gym_data: GymCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a new gym to the database."""
    # Check if gym already exists
    existing = db.query(Gym).filter(Gym.name == gym_data.name, Gym.address == gym_data.address).first()
    if existing:
        raise HTTPException(status_code=400, detail="Gym already exists at this location")
        
    new_gym = Gym(**gym_data.model_dump())
    db.add(new_gym)
    db.commit()
    db.refresh(new_gym)
    
    return new_gym

@router.post("/{gym_id}/check-in")
def check_in_gym(
    gym_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Set this gym as the user's preferred gym."""
    gym = db.query(Gym).filter(Gym.id == gym_id).first()
    if not gym:
        raise HTTPException(status_code=404, detail="Gym not found")
        
    profile = current_user.fitness_profile
    if not profile:
        raise HTTPException(status_code=400, detail="Please complete fitness profile first")
        
    profile.preferred_gym_id = gym.id
    db.commit()
    
    return {"message": f"Checked into {gym.name} successfully."}
