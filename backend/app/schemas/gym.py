from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GymBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: bool = True

class GymCreate(GymBase):
    pass

class GymResponse(GymBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GymRecommendationResponse(GymResponse):
    distance_km: Optional[float] = None
    member_count: int = 0
