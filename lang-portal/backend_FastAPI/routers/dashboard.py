from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import get_db
from models import StudySession, WordReviewItem, Group, StudyActivity, Word

router = APIRouter()


@router.get("/last_study_session")
async def get_last_study_session(db: Session = Depends(get_db)):
    """GET /api/dashboard/last_study_session"""
    last_session = db.query(StudySession).order_by(desc(StudySession.created_at)).first()
    
    if not last_session:
        raise HTTPException(status_code=404, detail="No study sessions found")
    
    return {
        "id": last_session.id,
        "group_id": last_session.group_id,
        "study_activity_id": last_session.study_activity_id,
        "group_name": last_session.group.name,
        "created_at": last_session.created_at.isoformat() + "Z"
    }


@router.get("/study_progress")
async def get_study_progress(db: Session = Depends(get_db)):
    """GET /api/dashboard/study_progress
    Returns study progress statistics.
    Frontend will determine progress bar based on total words studied and total available words
    """
    # Get unique words that have been reviewed (studied)
    total_words_studied = db.query(func.count(func.distinct(WordReviewItem.word_id))).scalar() or 0
    
    # Get total available words in database
    total_available_words = db.query(func.count(Word.id)).scalar() or 0
    
    return {
        "total_words_studied": total_words_studied,
        "total_available_words": total_available_words
    }


@router.get("/quick_stats")
async def get_quick_stats(db: Session = Depends(get_db)):
    """GET /api/dashboard/quick_stats
    Returns quick overview statistics
    """
    # Calculate success rate (percentage of correct reviews)
    total_reviews = db.query(func.count(WordReviewItem.id)).scalar() or 0
    correct_reviews = db.query(func.count(WordReviewItem.id)).filter(
        WordReviewItem.correct == True
    ).scalar() or 0
    
    success_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0.0
    
    # Total study sessions
    total_study_sessions = db.query(func.count(StudySession.id)).scalar() or 0
    
    # Total active groups (groups that have had study sessions)
    total_active_groups = db.query(func.count(func.distinct(StudySession.group_id))).scalar() or 0
    
    # Study streak days - simplified calculation (count distinct dates with sessions)
    # Note: This is a simplified version. Real streak calculation would need more complex logic
    study_streak_days = db.query(
        func.count(func.distinct(func.date(StudySession.created_at)))
    ).scalar() or 0
    
    return {
        "success_rate": round(success_rate, 1),
        "total_study_sessions": total_study_sessions,
        "total_active_groups": total_active_groups,
        "study_streak_days": study_streak_days
    }