"""
User Model
Authentication and basic profile fields
"""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    """
    User model with authentication and profile fields.
    """
    __tablename__ = "users"

    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile fields
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Status fields
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    fitness_profile = relationship(
        "FitnessProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.email}>"
