"""
WorkoutSession Model
Logs individual workout sessions
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class WorkoutSession(BaseModel):
    """
    WorkoutSession model for logging completed workouts.
    """
    __tablename__ = "workout_sessions"

    # Foreign keys
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    plan_id = Column(
        String(36),
        ForeignKey("workout_plans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Session details
    date = Column(Date, nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Basic metrics
    calories_burned = Column(Integer, nullable=True)
    exercises_completed = Column(Integer, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Mood/Energy (1-5 scale)
    energy_level = Column(Integer, nullable=True)
    mood_after = Column(Integer, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="workout_sessions")
    plan = relationship("WorkoutPlan", back_populates="sessions")

    def __repr__(self):
        return f"<WorkoutSession {self.date} user={self.user_id}>"
