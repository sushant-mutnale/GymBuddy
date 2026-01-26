"""
Matching Router
Endpoints for partner matching functionality
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List

from app.database import get_db
from app.models import User, Match, MatchStatus
from app.schemas.matching import MatchRecommendation, MatchResponse, MatchRequestCreate
from app.dependencies import get_current_user
from app.services.matching_service import MatchingService

router = APIRouter(prefix="/matches", tags=["Matches"])
matching_service = MatchingService()


@router.get("/recommendations", response_model=List[MatchRecommendation])
def get_recommendations(
    limit: int = Query(default=10, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get top N match recommendations for the current user."""
    recommendations = matching_service.get_match_recommendations(db, current_user.id, limit)
    
    result = []
    for rec in recommendations:
        candidate = rec["user"]
        profile = candidate.fitness_profile
        result.append(MatchRecommendation(
            user_id=candidate.id,
            full_name=candidate.full_name,
            avatar_url=candidate.avatar_url,
            score=rec["score"],
            breakdown=rec["breakdown"],
            fitness_level=profile.fitness_level if profile else None,
            goals=profile.goals if profile else [],
            bio=profile.bio if profile else None,
        ))
    
    return result


@router.post("/{candidate_id}/request", status_code=status.HTTP_201_CREATED)
def send_match_request(
    candidate_id: str,
    request_data: MatchRequestCreate = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send a match request to another user."""
    # Validate candidate exists
    candidate = db.query(User).filter(User.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="User not found")
    
    if candidate_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot match with yourself")
    
    # Check if match already exists (either direction)
    existing = db.query(Match).filter(
        or_(
            and_(Match.user_a_id == current_user.id, Match.user_b_id == candidate_id),
            and_(Match.user_a_id == candidate_id, Match.user_b_id == current_user.id),
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Match already exists")
    
    # Calculate match score
    score_data = matching_service.calculate_match_score(current_user, candidate)
    
    # Create match (user_a is the requester)
    match = Match(
        user_a_id=current_user.id,
        user_b_id=candidate_id,
        overall_score=score_data["overall_score"],
        score_breakdown=score_data["breakdown"],
        status=MatchStatus.PENDING.value,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    
    return {"message": "Match request sent", "match_id": match.id}


@router.post("/{match_id}/accept")
def accept_match(
    match_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Accept a pending match request."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Only the recipient (user_b) can accept
    if match.user_b_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to accept this match")
    
    if match.status != MatchStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Match is not pending")
    
    match.status = MatchStatus.ACCEPTED.value
    db.commit()
    
    return {"message": "Match accepted"}


@router.post("/{match_id}/reject")
def reject_match(
    match_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Reject a pending match request."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Only the recipient (user_b) can reject
    if match.user_b_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to reject this match")
    
    if match.status != MatchStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Match is not pending")
    
    match.status = MatchStatus.REJECTED.value
    db.commit()
    
    return {"message": "Match rejected"}


@router.get("", response_model=List[MatchResponse])
def list_matches(
    status_filter: str = Query(default=None, description="Filter by status: pending, accepted, rejected"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all matches for the current user."""
    query = db.query(Match).filter(
        or_(Match.user_a_id == current_user.id, Match.user_b_id == current_user.id)
    )
    
    if status_filter:
        query = query.filter(Match.status == status_filter)
    
    matches = query.order_by(Match.created_at.desc()).all()
    
    result = []
    for m in matches:
        # Determine partner
        if m.user_a_id == current_user.id:
            partner = m.user_b
        else:
            partner = m.user_a
        
        result.append(MatchResponse(
            id=m.id,
            user_a_id=m.user_a_id,
            user_b_id=m.user_b_id,
            overall_score=m.overall_score,
            score_breakdown=m.score_breakdown,
            status=m.status,
            created_at=m.created_at,
            updated_at=m.updated_at,
            partner_name=partner.full_name if partner else None,
            partner_avatar=partner.avatar_url if partner else None,
        ))
    
    return result
