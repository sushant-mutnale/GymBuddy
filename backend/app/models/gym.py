"""
Gym Model
Gym/fitness center information
"""

from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Gym(BaseModel):
    """
    Gym model with location and details.
    """
    __tablename__ = "gyms"

    # Basic info
    name = Column(String(200), nullable=False, index=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True, index=True)
    
    # Location coordinates (optional)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    members = relationship("FitnessProfile", back_populates="preferred_gym")

    def __repr__(self):
        return f"<Gym {self.name}>"
