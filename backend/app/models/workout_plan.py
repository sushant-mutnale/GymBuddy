"""
WorkoutPlan Model
Stores workout plans/routines for users
"""

from sqlalchemy import Column, String, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
import enum

from app.models.base import BaseModel


class PlanStatus(str, enum.Enum):
    """Workout plan status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class WorkoutPlan(BaseModel):
    """
    WorkoutPlan model for user workout routines.
    """
    __tablename__ = "workout_plans"

    # Foreign key to User
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Plan details
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Plan structure (JSON)
    # Example: {"days": [{"day": "monday", "exercises": [...]}, ...]}
    plan_data = Column(JSON, nullable=False, default=dict)
    
    # Duration
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Status
    status = Column(
        String(20),
        default=PlanStatus.ACTIVE.value,
        nullable=False,
        index=True,
    )
    
    # Plan type (e.g., "3-day split", "full body", "push-pull-legs")
    plan_type = Column(String(50), nullable=True)
    
    # Target goal (links to fitness goals)
    target_goal = Column(String(50), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="workout_plans")
    sessions = relationship("WorkoutSession", back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WorkoutPlan {self.name} for user={self.user_id}>"
