from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from database import get_db
from models import StudyActivity, StudySession, WordReviewItem, Group
from schemas import StudyActivityResponse, PaginationInfo

import math

router = APIRouter()


def create_pagination(current_page: int, total_items: int, items_per_page: int):
    total_pages = math.ceil(total_items / items_per_page) if total_items > 0 else 1
    return PaginationInfo(
        current_page=current_page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )


@router.get("/study_activities")
async def get_study_activities(db: Session = Depends(get_db)):
    activities = db.query(StudyActivity).all()

    items = []
    for activity in activities:
        items.append({
            "id": activity.id,
            "name": activity.name,
            "thumbnail": activity.thumbnail,
            "url": activity.url
        })

    return {"items": items}


@router.get("/study_activities/{activity_id}")
async def get_study_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(StudyActivity).filter(StudyActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Study activity not found")

    return {
        "id": activity.id,
        "name": activity.name,
        "thumbnail": activity.thumbnail,
        "description": activity.description,
        "url": activity.url
    }


@router.get("/study_activities/{activity_id}/study_sessions")
async def get_activity_study_sessions(
    activity_id: int,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    items_per_page = 20
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(StudySession.id)).filter(
        StudySession.study_activity_id == activity_id
    ).scalar()

    sessions = db.query(StudySession).filter(
        StudySession.study_activity_id == activity_id
    ).offset(offset).limit(items_per_page).all()

    items = []
    for session in sessions:
        review_count = db.query(func.count(WordReviewItem.study_session_id)).filter(
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


# MOVED FROM study_sessions.py - This route belongs here according to specs
@router.post("/study_activities")
async def create_study_session(
    group_id: int = Query(...),
    study_activity_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """POST /api/study_activities
    Request Params: group_id integer, study_activity_id integer
    Creates a new study session for the specified group and activity
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    activity = db.query(StudyActivity).filter(StudyActivity.id == study_activity_id).first()

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not activity:
        raise HTTPException(status_code=404, detail="Study activity not found")

    session = StudySession(
        group_id=group_id,
        study_activity_id=study_activity_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "id": session.id,
        "group_id": session.group_id
    }