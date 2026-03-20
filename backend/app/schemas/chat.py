from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    match_id: str

class MessageResponse(MessageBase):
    id: str
    match_id: str
    sender_id: str
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRoomResponse(BaseModel):
    match_id: str
    partner_id: str
    partner_name: str
    partner_avatar: Optional[str] = None
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0
