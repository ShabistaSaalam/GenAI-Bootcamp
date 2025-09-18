from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from database import get_db
from models import Group, WordGroup, WordReviewItem, Word, StudySession
from schemas import GroupResponse, WordResponse, PaginationInfo

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


@router.get("/groups")
async def get_groups(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    items_per_page = 20
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(Group.id)).scalar()
    groups = db.query(Group).offset(offset).limit(items_per_page).all()

    items = []
    for group in groups:
        word_count = db.query(func.count(WordGroup.word_id)).filter(
            WordGroup.group_id == group.id
        ).scalar()

        items.append(GroupResponse(
            id=group.id,
            name=group.name,
            word_count=word_count
        ))

    return {
        "items": items,
        "pagination": create_pagination(page, total_items, items_per_page)
    }


@router.get("/groups/{group_id}")
async def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    word_count = db.query(func.count(WordGroup.word_id)).filter(
        WordGroup.group_id == group.id
    ).scalar()

    return {
        "id": group.id,
        "name": group.name,
        "stats": {"total_word_count": word_count}
    }


@router.get("/groups/{group_id}/words")
async def get_group_words(
    group_id: int,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    items_per_page = 100
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(Word.id)).join(WordGroup).filter(
        WordGroup.group_id == group_id
    ).scalar()

    words = db.query(Word).join(WordGroup).filter(
        WordGroup.group_id == group_id
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


@router.get("/groups/{group_id}/study_sessions")
async def get_group_study_sessions(
    group_id: int,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """GET /api/groups/:id/study_sessions
    Returns all study sessions for a specific group with pagination
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    items_per_page = 20
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(StudySession.id)).filter(
        StudySession.group_id == group_id
    ).scalar()

    sessions = db.query(StudySession).filter(
        StudySession.group_id == group_id
    ).offset(offset).limit(items_per_page).all()

    items = []
    for session in sessions:
        review_count = db.query(func.count(WordReviewItem.id)).filter(
            WordReviewItem.study_session_id == session.id
        ).scalar()

        items.append({
            "id": session.id,
            "activity_name": session.activity.name,
            "group_name": session.group.name,
            "start_time": session.created_at.isoformat() + "Z",
            "end_time": (session.ended_at or datetime.utcnow()).isoformat() + "Z", 
            "review_items_count": review_count
        })

    return {
        "items": items,
        "pagination": create_pagination(page, total_items, items_per_page)
    }