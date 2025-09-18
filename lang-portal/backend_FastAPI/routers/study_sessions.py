from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from database import get_db
from models import (
    StudySession,
    WordReviewItem,
    Word,
    Group,
    StudyActivity,
    WordGroup
)
from schemas import (
    ReviewRequest,
    WordResponse,
    PaginationInfo
)
import math

router = APIRouter()


def get_word_stats(db: Session, word_id: int):
    correct_count = db.query(func.count(WordReviewItem.word_id)).filter(
        WordReviewItem.word_id == word_id,
        WordReviewItem.correct == True
    ).scalar() or 0

    wrong_count = db.query(func.count(WordReviewItem.word_id)).filter(
        WordReviewItem.word_id == word_id,
        WordReviewItem.correct == False
    ).scalar() or 0

    return correct_count, wrong_count


def create_pagination(current_page: int, total_items: int, items_per_page: int):
    total_pages = math.ceil(total_items / items_per_page) if total_items > 0 else 1
    return PaginationInfo(
        current_page=current_page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )


def format_session_times(session):
    """Helper function to format session start and end times properly"""
    start_time = session.created_at.isoformat() + "Z"
    
    if session.ended_at:
        # Session has ended
        end_time = session.ended_at.isoformat() + "Z"
    else:
        # Session is still active - use current time or None
        # For API consistency, we'll use current time
        end_time = datetime.utcnow().isoformat() + "Z"
    
    return start_time, end_time


@router.get("/study_sessions")
async def get_study_sessions(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    items_per_page = 100
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(StudySession.id)).scalar()
    sessions = db.query(StudySession).offset(offset).limit(items_per_page).all()

    items = []
    for session in sessions:
        review_count = db.query(func.count(WordReviewItem.study_session_id)).filter(
            WordReviewItem.study_session_id == session.id
        ).scalar()

        start_time, end_time = format_session_times(session)

        items.append({
            "id": session.id,
            "activity_name": session.activity.name,
            "group_name": session.group.name,
            "start_time": start_time,
            "end_time": end_time,
            "review_items_count": review_count
        })

    return {
        "items": items,
        "pagination": create_pagination(page, total_items, items_per_page)
    }


@router.get("/study_session/{session_id}")
async def get_study_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")

    review_count = db.query(func.count(WordReviewItem.study_session_id)).filter(
        WordReviewItem.study_session_id == session.id
    ).scalar()

    start_time, end_time = format_session_times(session)

    return {
        "id": session.id,
        "activity_name": session.activity.name,
        "group_name": session.group.name,
        "start_time": start_time,
        "end_time": end_time,
        "review_items_count": review_count
    }


@router.get("/study_session/{session_id}/words")
async def get_study_session_words(
    session_id: int,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")

    items_per_page = 100
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(Word.id)).join(WordGroup).filter(
        WordGroup.group_id == session.group_id
    ).scalar()

    words = db.query(Word).join(WordGroup).filter(
        WordGroup.group_id == session.group_id
    ).offset(offset).limit(items_per_page).all()

    items = []
    for word in words:
        correct_count, wrong_count = get_word_stats(db, word.id)
        items.append(WordResponse(
            korean=word.korean,
            transliteration=word.transliteration,
            english=word.english,
            correct_count=correct_count,
            wrong_count=wrong_count
        ))

    return {
        "items": items,
        "pagination": create_pagination(page, total_items, items_per_page)
    }


@router.post("/study_sessions/{session_id}/words/{word_id}/review")
async def create_word_review(
    session_id: int,
    word_id: int,
    review: ReviewRequest,
    db: Session = Depends(get_db)
):
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    word = db.query(Word).filter(Word.id == word_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    review_item = WordReviewItem(
        word_id=word_id,
        study_session_id=session_id,
        correct=review.correct
    )

    db.add(review_item)
    db.commit()

    return {
        "success": True,
        "word_id": word_id,
        "study_session_id": session_id,
        "correct": review.correct,
        "created_at": review_item.created_at.isoformat() + "Z"
    }


# NEW ENDPOINT: End a study session
@router.post("/study_sessions/{session_id}/end")
async def end_study_session(session_id: int, db: Session = Depends(get_db)):
    """End a study session by setting ended_at timestamp"""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    if session.ended_at:
        raise HTTPException(status_code=400, detail="Study session already ended")
    
    session.ended_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "session_id": session_id,
        "ended_at": session.ended_at.isoformat() + "Z"
    }


@router.post("/reset/history")
async def reset_history(db: Session = Depends(get_db)):
    db.query(WordReviewItem).delete()
    db.query(StudySession).delete()
    db.commit()

    return {
        "success": True,
        "message": "Study history reset successfully"
    }


@router.post("/full_reset")
async def full_reset(db: Session = Depends(get_db)):
    from models import WordGroup, Group, Word, StudyActivity

    db.query(WordReviewItem).delete()
    db.query(StudySession).delete()
    db.query(WordGroup).delete()
    db.query(Word).delete()
    db.query(Group).delete()
    db.query(StudyActivity).delete()
    db.commit()

    return {
        "success": True,
        "message": "Full reset completed successfully"
    }