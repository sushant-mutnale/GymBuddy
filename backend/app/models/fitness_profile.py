"""
FitnessProfile Model
User fitness preferences and goals
"""

from sqlalchemy import Column, String, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
import enum

from app.models.base import BaseModel


class FitnessLevel(str, enum.Enum):
    """User fitness level enum"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class PreferredSchedule(str, enum.Enum):
    """Preferred workout time enum"""
    EARLY_MORNING = "early_morning"  # 5-7 AM
    MORNING = "morning"              # 7-10 AM
    AFTERNOON = "afternoon"          # 12-5 PM
    EVENING = "evening"              # 5-8 PM
    NIGHT = "night"                  # 8-11 PM


class FitnessProfile(BaseModel):
    """
    FitnessProfile model with workout preferences and goals.
    One-to-one relationship with User.
    """
    __tablename__ = "fitness_profiles"

    # Foreign key to User
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    
    # Fitness level
    fitness_level = Column(
        String(20),
        default=FitnessLevel.BEGINNER.value,
        nullable=False,
    )
    
    # Goals (JSON array: e.g., ["build_muscle", "lose_weight", "cardio"])
    goals = Column(JSON, default=list, nullable=False)
    
    # Workout types (JSON array: e.g., ["strength", "hiit", "yoga"])
    workout_types = Column(JSON, default=list, nullable=False)
    
    # Schedule preferences
    preferred_schedule = Column(
        String(20),
        default=PreferredSchedule.MORNING.value,
        nullable=False,
    )
    
    # Preferred days (JSON array: e.g., ["monday", "wednesday", "friday"])
    preferred_days = Column(JSON, default=list, nullable=False)
    
    # Preferred gym (optional)
    preferred_gym_id = Column(
        String(36),
        ForeignKey("gyms.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Personal details
    gender = Column(String(20), nullable=True)  # male, female, other
    age = Column(Integer, nullable=True)

    # Bio/description
    bio = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="fitness_profile")
    preferred_gym = relationship("Gym", back_populates="members")

    def __repr__(self):
        return f"<FitnessProfile user_id={self.user_id}>"
