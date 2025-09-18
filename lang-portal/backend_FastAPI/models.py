from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    korean = Column(String(200), nullable=False)
    transliteration = Column(String(200), nullable=False)
    english = Column(String(200), nullable=False)
    parts = Column(JSON, default=dict)

    groups = relationship("Group", secondary="words_groups", back_populates="words")
    review_items = relationship("WordReviewItem", back_populates="word")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    words = relationship("Word", secondary="words_groups", back_populates="groups")
    study_sessions = relationship("StudySession", back_populates="group")


class WordGroup(Base):
    __tablename__ = "words_groups"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)


class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    thumbnail = Column(String(255))
    description = Column(Text)
    url = Column(String(255))

    study_sessions = relationship("StudySession", back_populates="activity")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # ADDED: End time tracking for proper session duration
    ended_at = Column(DateTime, nullable=True)  # Null means session is still active

    group = relationship("Group", back_populates="study_sessions")
    activity = relationship("StudyActivity", back_populates="study_sessions")
    review_items = relationship("WordReviewItem", back_populates="study_session")


class WordReviewItem(Base):
    __tablename__ = "word_review_items"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    word = relationship("Word", back_populates="review_items")
    study_session = relationship("StudySession", back_populates="review_items")