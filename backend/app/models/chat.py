"""
Chat Model
Stores messages exchanged between matched users
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.models.base import BaseModel


class Message(BaseModel):
    """
    Message model representing a direct message within a Match.
    """
    __tablename__ = "messages"

    # Match ID specifies the 'room'
    match_id = Column(
        String(36),
        ForeignKey("matches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Sender ID
    sender_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Message Content
    content = Column(Text, nullable=False)
    
    # Meta
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)

    # Relationships
    match = relationship("Match")
    sender = relationship("User", foreign_keys=[sender_id])

    def mark_read(self):
        self.is_read = True
        self.read_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f"<Message {self.id} in Match {self.match_id}>"
