from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Dict

from app.database import get_db
from app.models import User, Match, Message, MatchStatus
from app.schemas.chat import MessageResponse, ChatRoomResponse, MessageCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

class ConnectionManager:
    def __init__(self):
        # Maps match_id to a list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, match_id: str):
        await websocket.accept()
        if match_id not in self.active_connections:
            self.active_connections[match_id] = []
        self.active_connections[match_id].append(websocket)

    def disconnect(self, websocket: WebSocket, match_id: str):
        if match_id in self.active_connections:
            self.active_connections[match_id].remove(websocket)
            if not self.active_connections[match_id]:
                del self.active_connections[match_id]

    async def broadcast_to_match(self, message: dict, match_id: str):
        if match_id in self.active_connections:
            for connection in self.active_connections[match_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.get("/rooms", response_model=List[ChatRoomResponse])
def get_chat_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chat rooms (accepted matches) for the user."""
    matches = db.query(Match).filter(
        or_(Match.user_a_id == current_user.id, Match.user_b_id == current_user.id),
        Match.status == MatchStatus.ACCEPTED.value
    ).all()
    
    rooms = []
    for match in matches:
        partner = match.user_b if match.user_a_id == current_user.id else match.user_a
        
        # Get last message
        last_message = db.query(Message).filter(Message.match_id == match.id).order_by(Message.created_at.desc()).first()
        
        # Get unread count
        unread = db.query(Message).filter(
            Message.match_id == match.id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        ).count()
        
        last_msg_resp = None
        if last_message:
            last_msg_resp = MessageResponse(
                id=last_message.id,
                match_id=last_message.match_id,
                sender_id=last_message.sender_id,
                content=last_message.content,
                is_read=last_message.is_read,
                read_at=last_message.read_at,
                created_at=last_message.created_at
            )
            
        rooms.append(ChatRoomResponse(
            match_id=match.id,
            partner_id=partner.id,
            partner_name=partner.full_name,
            partner_avatar=partner.avatar_url,
            last_message=last_msg_resp,
            unread_count=unread
        ))
        
    # Sort rooms by last message time if available
    rooms.sort(key=lambda x: x.last_message.created_at if x.last_message else match.created_at, reverse=True)
    return rooms

@router.get("/{match_id}/messages", response_model=List[MessageResponse])
def get_messages(
    match_id: str,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get history of messages for a specific match/room."""
    # Verify match exists and user is part of it
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
        
    if match.user_a_id != current_user.id and match.user_b_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these messages")
        
    messages = db.query(Message).filter(Message.match_id == match_id).order_by(Message.created_at.desc()).offset(offset).limit(limit).all()
    
    # Mark as read the ones sent by partner
    unread_messages = [m for m in messages if m.sender_id != current_user.id and not m.is_read]
    for m in unread_messages:
        m.mark_read()
    if unread_messages:
        db.commit()
    
    # Return reversed to show chronological order
    return messages[::-1]

@router.websocket("/ws/{match_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    match_id: str,
    db: Session = Depends(get_db),
    # In a real app with WebSockets, we would extract token from query or headers to authenticate
    # current_user: User = Depends(get_current_user)
    # For now, we'll accept the user_id in the JSON payload or query param for simplicity.
):
    await manager.connect(websocket, match_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Expecting data format: {"sender_id": str, "content": str}
            sender_id = data.get("sender_id")
            content = data.get("content")
            
            if not sender_id or not content:
                continue
                
            # Save to DB
            new_message = Message(
                match_id=match_id,
                sender_id=sender_id,
                content=content
            )
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            
            # Broadcast to all connected clients in this room (both users if online)
            msg_payload = {
                "id": new_message.id,
                "match_id": match_id,
                "sender_id": sender_id,
                "content": content,
                "created_at": new_message.created_at.isoformat(),
                "is_read": False
            }
            await manager.broadcast_to_match(msg_payload, match_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, match_id)
