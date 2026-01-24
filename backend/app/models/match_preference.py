"""
MatchPreference Model
User preferences for finding partners
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class GenderPreference(str, enum.Enum):
    """Gender preference enum"""
    MALE = "male"
    FEMALE = "female"
    ANY = "any"


class MatchPreference(BaseModel):
    """
    MatchPreference model for user discovery settings.
    One-to-one relationship with User.
    """
    __tablename__ = "match_preferences"

    # Foreign key to User
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    
    # Preferences
    gender_preference = Column(
        String(20),
        default=GenderPreference.ANY.value,
        nullable=False,
    )
    
    min_age = Column(Integer, default=18, nullable=False)
    max_age = Column(Integer, default=100, nullable=False)
    
    max_distance_km = Column(Integer, default=50, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="match_preference")

    def __repr__(self):
        return f"<MatchPreference user_id={self.user_id}>"
