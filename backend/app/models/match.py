"""
Match Model
Stores compatibility scores and match status between two users
"""

from sqlalchemy import Column, String, Float, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
import enum

from app.models.base import BaseModel


class MatchStatus(str, enum.Enum):
    """Match status enum"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Match(BaseModel):
    """
    Match model representing a potential or active match between two users.
    """
    __tablename__ = "matches"

    # Users involved in the match
    user_a_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_b_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Match score
    overall_score = Column(Float, nullable=False, index=True)
    score_breakdown = Column(JSON, default=dict, nullable=False)
    
    # Status
    status = Column(
        String(20),
        default=MatchStatus.PENDING.value,
        nullable=False,
        index=True,
    )
    
    # Relationships
    user_a = relationship("User", foreign_keys=[user_a_id])
    user_b = relationship("User", foreign_keys=[user_b_id])

    # Ensure uniqueness of the pair (user_a < user_b convention enforced in service)
    # but DB constraint helps too.
    __table_args__ = (
        UniqueConstraint('user_a_id', 'user_b_id', name='unique_match_pair'),
    )

    def __repr__(self):
        return f"<Match {self.user_a_id}-{self.user_b_id} score={self.overall_score}>"
