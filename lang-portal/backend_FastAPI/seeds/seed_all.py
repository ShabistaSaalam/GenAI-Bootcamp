import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Word, Group, WordGroup, StudyActivity, StudySession, WordReviewItem

def clear_all_data(db: Session):
    """Clear all data from database"""
    print("🗑️  Clearing existing data...")
    db.query(WordReviewItem).delete()
    db.query(StudySession).delete()
    db.query(WordGroup).delete()
    db.query(Word).delete()
    db.query(Group).delete()
    db.query(StudyActivity).delete()
    db.commit()
    print("✅ Database cleared")

def seed_study_activities(db: Session):
    """Seed study activities"""
    print("📚 Seeding study activities...")
    
    activities = [
        {
            "name": "Vocabulary Quiz",
            "thumbnail": "/thumbnails/vocabulary.png",
            "description": "Practice vocabulary with digital flash cards",
            "url": "https://flashcards.app/launch"
        },
        {
            "name": "Listening Practice",
            "thumbnail": "/thumbnails/listening.png",
            "description": "Improve listening skills with audio exercises",
            "url": "https://listening.app/launch"
        },
        {
            "name": "Speaking Practice",
            "thumbnail": "/thumbnails/speaking.png",
            "description": "Practice pronunciation and speaking skills",
            "url": "https://speaking.app/launch"
        },
        {
            "name": "Grammar Quiz",
            "thumbnail": "/thumbnails/grammar.png",
            "description": "Test your Korean grammar knowledge",
            "url": "https://grammar.app/launch"
        }
    ]
    
    for activity_data in activities:
        activity = StudyActivity(**activity_data)
        db.add(activity)
    
    db.commit()
    print(f"✅ Added {len(activities)} study activities")

def seed_groups(db: Session):
    """Seed word groups"""
    print("🏷️  Seeding groups...")
    
    groups = [
        "Basic Greetings",
        "Food & Dining", 
        "Numbers",
        "Colors",
        "Family",
        "Time & Dates",
        "Transportation",
        "Weather",
        "Body Parts",
        "Emotions"
    ]
    
    for group_name in groups:
        group = Group(name=group_name)
        db.add(group)
    
    db.commit()
    print(f"✅ Added {len(groups)} groups")

def seed_words(db: Session):
    """Seed Korean words with dummy data"""
    print("📝 Seeding words...")
    
    # Sample Korean words organized by group
    words_data = {
        "Basic Greetings": [
            {"korean": "안녕하세요", "transliteration": "annyeonghaseyo", "english": "hello"},
            {"korean": "안녕히가세요", "transliteration": "annyeonghi gaseyo", "english": "goodbye (to person leaving)"},
            {"korean": "감사합니다", "transliteration": "gamsahamnida", "english": "thank you"},
            {"korean": "죄송합니다", "transliteration": "joesonghamnida", "english": "I'm sorry"},
            {"korean": "처음 뵙겠습니다", "transliteration": "cheoeum boepgesseumnida", "english": "nice to meet you"}
        ],
        "Food & Dining": [
            {"korean": "김치", "transliteration": "gimchi", "english": "kimchi"},
            {"korean": "비빔밥", "transliteration": "bibimbap", "english": "mixed rice bowl"},
            {"korean": "불고기", "transliteration": "bulgogi", "english": "Korean BBQ"},
            {"korean": "라면", "transliteration": "ramyeon", "english": "instant noodles"},
            {"korean": "한식", "transliteration": "hansik", "english": "Korean food"},
            {"korean": "맛있다", "transliteration": "masitda", "english": "delicious"},
            {"korean": "먹다", "transliteration": "meokda", "english": "to eat"}
        ],
        "Numbers": [
            {"korean": "하나", "transliteration": "hana", "english": "one"},
            {"korean": "둘", "transliteration": "dul", "english": "two"},
            {"korean": "셋", "transliteration": "set", "english": "three"},
            {"korean": "넷", "transliteration": "net", "english": "four"},
            {"korean": "다섯", "transliteration": "daseot", "english": "five"}
        ],
        "Colors": [
            {"korean": "빨간색", "transliteration": "ppalgansaek", "english": "red"},
            {"korean": "파란색", "transliteration": "paransaek", "english": "blue"},
            {"korean": "노란색", "transliteration": "noransaek", "english": "yellow"},
            {"korean": "검은색", "transliteration": "geomeunsaek", "english": "black"},
            {"korean": "하얀색", "transliteration": "hayansaek", "english": "white"}
        ],
        "Family": [
            {"korean": "아버지", "transliteration": "abeoji", "english": "father"},
            {"korean": "어머니", "transliteration": "eomeoni", "english": "mother"},
            {"korean": "형", "transliteration": "hyeong", "english": "older brother (male speaker)"},
            {"korean": "누나", "transliteration": "nuna", "english": "older sister (male speaker)"},
            {"korean": "동생", "transliteration": "dongsaeng", "english": "younger sibling"}
        ]
    }
    
    # Get all groups
    groups = {g.name: g for g in db.query(Group).all()}
    
    word_count = 0
    for group_name, word_list in words_data.items():
        if group_name in groups:
            group = groups[group_name]
            
            for word_data in word_list:
                # Create word
                word = Word(
                    korean=word_data["korean"],
                    transliteration=word_data["transliteration"],
                    english=word_data["english"],
                    parts={}
                )
                db.add(word)
                db.commit()
                db.refresh(word)
                
                # Link word to group
                word_group = WordGroup(word_id=word.id, group_id=group.id)
                db.add(word_group)
                
                word_count += 1
    
    db.commit()
    print(f"✅ Added {word_count} words")

def seed_study_sessions(db: Session):
    """Seed study sessions with realistic timestamps"""
    print("🎯 Seeding study sessions...")
    
    # Get all groups and activities
    groups = db.query(Group).all()
    activities = db.query(StudyActivity).all()
    
    if not groups or not activities:
        print("❌ No groups or activities found. Seed them first.")
        return
    
    # Create sessions over the past 2 weeks
    sessions_created = 0
    base_date = datetime.now() - timedelta(days=14)
    
    for i in range(15):  # Create 15 sessions
        session_date = base_date + timedelta(days=i)
        
        # Pick random group and activity
        group = groups[i % len(groups)]
        activity = activities[i % len(activities)]
        
        session = StudySession(
            group_id=group.id,
            study_activity_id=activity.id,
            created_at=session_date,
            ended_at=session_date + timedelta(minutes=15)  # 15-minute sessions
        )
        
        db.add(session)
        sessions_created += 1
    
    db.commit()
    print(f"✅ Added {sessions_created} study sessions")

def seed_word_reviews(db: Session):
    """Seed word review items"""
    print("📊 Seeding word review items...")
    
    # Get all sessions and words
    sessions = db.query(StudySession).all()
    
    if not sessions:
        print("❌ No study sessions found. Seed them first.")
        return
    
    reviews_created = 0
    
    for session in sessions:
        # Get words from the session's group
        words = db.query(Word).join(WordGroup).filter(
            WordGroup.group_id == session.group_id
        ).limit(10).all()  # Review up to 10 words per session
        
        for word in words:
            # Create 1-3 review items per word with mixed results
            import random
            num_reviews = random.randint(1, 3)
            
            for _ in range(num_reviews):
                correct = random.choice([True, True, True, False])  # 75% success rate
                
                review = WordReviewItem(
                    word_id=word.id,
                    study_session_id=session.id,
                    correct=correct,
                    created_at=session.created_at + timedelta(minutes=random.randint(1, 14))
                )
                
                db.add(review)
                reviews_created += 1
    
    db.commit()
    print(f"✅ Added {reviews_created} word review items")

def main():
    """Main seeding function"""
    print("🌱 Starting database seeding with dummy data...")
    
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_all_data(db)
        
        # Seed in order (respecting foreign key constraints)
        seed_study_activities(db)
        seed_groups(db)
        seed_words(db)
        seed_study_sessions(db)
        seed_word_reviews(db)
        
        # Print final statistics
        print("\n🎉 Seeding completed!")
        print("=" * 40)
        print(f"Study Activities: {db.query(StudyActivity).count()}")
        print(f"Groups: {db.query(Group).count()}")
        print(f"Words: {db.query(Word).count()}")
        print(f"Word-Group Links: {db.query(WordGroup).count()}")
        print(f"Study Sessions: {db.query(StudySession).count()}")
        print(f"Word Reviews: {db.query(WordReviewItem).count()}")
        print("=" * 40)
        print("🚀 Ready to test all API endpoints!")
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()