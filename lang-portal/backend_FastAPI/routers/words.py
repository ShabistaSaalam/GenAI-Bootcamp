# routers/words.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Word, WordReviewItem
from schemas import WordResponse, WordDetailResponse, WordStats, GroupInfo, PaginationInfo

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


@router.get("/words")
async def get_words(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    items_per_page = 100
    offset = (page - 1) * items_per_page

    total_items = db.query(func.count(Word.id)).scalar()
    words = db.query(Word).offset(offset).limit(items_per_page).all()

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


@router.get("/words/{word_id}")
async def get_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    correct_count, wrong_count = get_word_stats(db, word.id)

    # FIXED: Now properly typed as List[GroupInfo] instead of List[dict]
    groups = [GroupInfo(id=group.id, name=group.name) for group in word.groups]

    return WordDetailResponse(
        korean=word.korean,
        transliteration=word.transliteration,
        english=word.english,
        stats=WordStats(correct_count=correct_count, wrong_count=wrong_count),
        groups=groups
    )