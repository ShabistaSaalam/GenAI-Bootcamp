from pydantic import BaseModel
from typing import List, Optional


# ---------- Pagination ----------
class PaginationInfo(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int


# ---------- Word ----------
class WordStats(BaseModel):
    correct_count: int
    wrong_count: int


class WordResponse(BaseModel):
    korean: str
    transliteration: str
    english: str
    correct_count: int
    wrong_count: int


class GroupInfo(BaseModel):
    id: int
    name: str


class WordDetailResponse(BaseModel):
    korean: str
    transliteration: str
    english: str
    stats: WordStats
    groups: List[GroupInfo]  # FIXED: Was List[dict], now properly typed


class WordListResponse(BaseModel):
    items: List[WordResponse]
    pagination: PaginationInfo


# ---------- Group ----------
class GroupResponse(BaseModel):
    id: int
    name: str
    word_count: int


class GroupDetailResponse(BaseModel):
    id: int
    name: str
    stats: dict  # {"total_word_count": int}


class GroupListResponse(BaseModel):
    items: List[GroupResponse]
    pagination: PaginationInfo


class GroupWordsResponse(BaseModel):
    items: List[WordResponse]
    pagination: PaginationInfo


# ---------- Study Session ----------
class StudySessionResponse(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: str
    end_time: Optional[str]
    review_items_count: int


class StudySessionDetailResponse(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: str
    end_time: str
    review_items_count: int


class StudySessionListResponse(BaseModel):
    items: List[StudySessionResponse]
    pagination: PaginationInfo


class StudySessionWordsResponse(BaseModel):
    items: List[WordResponse]
    pagination: PaginationInfo


class GroupStudySessionsResponse(BaseModel):
    items: List[StudySessionResponse]
    pagination: PaginationInfo


# ---------- Study Activity ----------
class StudyActivityResponse(BaseModel):
    id: int
    name: str
    thumbnail: str
    url: str


class StudyActivityDetailResponse(BaseModel):
    id: int
    name: str
    thumbnail: str
    description: str
    url: str


class StudyActivityListResponse(BaseModel):
    items: List[StudyActivityResponse]


class StudyActivitySessionsResponse(BaseModel):
    items: List[StudySessionResponse]
    pagination: PaginationInfo


class StudyActivityCreateResponse(BaseModel):
    id: int
    group_id: int


# ---------- Dashboard ----------
class LastStudySessionResponse(BaseModel):
    id: int
    group_id: int
    study_activity_id: int
    group_name: str
    created_at: str


class StudyProgressResponse(BaseModel):
    total_words_studied: int
    total_available_words: int


class QuickStatsResponse(BaseModel):
    success_rate: float
    total_study_sessions: int
    total_active_groups: int
    study_streak_days: int


# ---------- Review ----------
class ReviewRequest(BaseModel):
    correct: bool


class ReviewResponse(BaseModel):
    success: bool
    word_id: int
    study_session_id: int
    correct: bool
    created_at: str


# ---------- Reset ----------
class ResetResponse(BaseModel):
    success: bool
    message: str

