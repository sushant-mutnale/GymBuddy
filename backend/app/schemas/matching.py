"""
Matching Schemas
Pydantic models for matching requests and responses
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class MatchStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class MatchRecommendation(BaseModel):
    """Recommendation response item."""
    user_id: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    score: float
    breakdown: Dict[str, float]
    fitness_level: Optional[str] = None
    goals: List[str] = []
    bio: Optional[str] = None


class MatchResponse(BaseModel):
    """Match response schema."""
    id: str
    user_a_id: str
    user_b_id: str
    overall_score: float
    score_breakdown: Dict
    status: str
    created_at: datetime
    updated_at: datetime
    
    # Partner info (populated based on perspective)
    partner_name: Optional[str] = None
    partner_avatar: Optional[str] = None

    class Config:
        from_attributes = True


class MatchRequestCreate(BaseModel):
    """Request to create a match request."""
    message: Optional[str] = None
