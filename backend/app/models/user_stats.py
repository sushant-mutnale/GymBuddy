"""
UserStats Model
Tracks user activity statistics for analytics
"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class UserStats(BaseModel):
    """
    UserStats model for tracking user activity.
    One-to-one relationship with User.
    """
    __tablename__ = "user_stats"

    # Foreign key to User
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    
    # Workout stats
    total_workouts = Column(Integer, default=0, nullable=False)
    total_duration_minutes = Column(Integer, default=0, nullable=False)
    total_calories_burned = Column(Integer, default=0, nullable=False)
    
    # Streak tracking
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_workout_date = Column(Date, nullable=True)
    
    # Match stats
    total_matches = Column(Integer, default=0, nullable=False)
    active_partners = Column(Integer, default=0, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="stats")

    def __repr__(self):
        return f"<UserStats user_id={self.user_id} workouts={self.total_workouts}>"
