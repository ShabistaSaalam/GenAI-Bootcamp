from invoke import task
import os
import json
import glob
from database import Base, engine, SessionLocal


@task
def init_db(c):
    """Initialize Database"""
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")


@task 
def migrate_db(c):
    """Migrate Database - run SQL files in migrations/ folder"""
    print("Running database migrations...")
    
    migrations_dir = "migrations"
    if not os.path.exists(migrations_dir):
        print(f"No {migrations_dir} directory found")
        return
    
    # Get all SQL files and sort by filename (0001_init.sql, 0002_create_tables.sql, etc.)
    sql_files = sorted(glob.glob(os.path.join(migrations_dir, "*.sql")))
    
    if not sql_files:
        print("No migration files found")
        return
    
    db = SessionLocal()
    try:
        for sql_file in sql_files:
            print(f"Running migration: {os.path.basename(sql_file)}")
            
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                db.execute(statement)
            
            db.commit()
            print(f"  ✅ {os.path.basename(sql_file)} completed")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Database migrations completed")


@task
def seed_study_activities(c):
    """Seed Study Activities from JSON file"""
    print("Seeding study activities...")
    
    from models import StudyActivity
    
    activities_file = "seeds/study_activities.json"
    if not os.path.exists(activities_file):
        print(f"Study activities file not found: {activities_file}")
        return
    
    db = SessionLocal()
    try:
        # Load activities from JSON
        with open(activities_file, 'r', encoding='utf-8') as f:
            activities_data = json.load(f)
        
        activities_added = 0
        for activity_data in activities_data:
            # Check if activity already exists
            existing = db.query(StudyActivity).filter(StudyActivity.name == activity_data['name']).first()
            if not existing:
                activity = StudyActivity(
                    name=activity_data['name'],
                    thumbnail=activity_data['thumbnail'],
                    description=activity_data['description'],
                    url=activity_data['url']
                )
                db.add(activity)
                activities_added += 1
                print(f"  ✅ Added activity: {activity_data['name']}")
            else:
                print(f"  - Activity already exists: {activity_data['name']}")
        
        db.commit()
        print(f"Study activities seeding completed: {activities_added} new activities added")
        
    except Exception as e:
        print(f"Study activities seeding failed: {e}")
        db.rollback()
    finally:
        db.close()


@task
def seed_data(c):
    """Seed Data - import JSON files from seeds/ folder"""
    print("Seeding database...")
    
    seeds_dir = "seeds"
    if not os.path.exists(seeds_dir):
        print(f"No {seeds_dir} directory found")
        return
    
    # Import models here to avoid circular imports - FIXED: WordsGroups -> WordGroup
    from models import Word, Group, WordGroup
    
    # Get all JSON files from seeds directory
    json_files = glob.glob(os.path.join(seeds_dir, "*.json"))
    
    if not json_files:
        print("No seed files found")
        return
    
    db = SessionLocal()
    try:
        # DSL: Map filename to group name
        # You can customize this mapping based on your seed file naming convention
        file_to_group_mapping = {
            "basic_greetings.json": "Basic Greetings",
            "food_dining.json": "Food & Dining", 
            "daily_conversations.json": "Daily Conversations",
            "numbers.json": "Numbers",
            "colors.json": "Colors"
        }
        
        for json_file in json_files:
            filename = os.path.basename(json_file)
            print(f"Processing seed file: {filename}")
            
            # Determine group name
            group_name = file_to_group_mapping.get(filename, 
                                                 filename.replace('.json', '').replace('_', ' ').title())
            
            # Create or get group
            group = db.query(Group).filter(Group.name == group_name).first()
            if not group:
                group = Group(name=group_name)
                db.add(group)
                db.commit()
                db.refresh(group)
            
            # Load and process words from JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                words_data = json.load(f)
            
            for word_data in words_data:
                # Check if word already exists
                existing_word = db.query(Word).filter(
                    Word.korean == word_data['korean']
                ).first()
                
                if not existing_word:
                    # Create new word
                    word = Word(
                        korean=word_data['korean'],
                        transliteration=word_data['transliteration'],
                        english=word_data['english'],
                        parts=word_data.get('parts', {})  # FIXED: Pass dict directly, not json.dumps()
                    )
                    db.add(word)
                    db.commit()
                    db.refresh(word)
                else:
                    word = existing_word
                
                # Link word to group (if not already linked) - FIXED: WordsGroups -> WordGroup
                existing_link = db.query(WordGroup).filter(
                    WordGroup.word_id == word.id,
                    WordGroup.group_id == group.id
                ).first()
                
                if not existing_link:
                    word_group_link = WordGroup(word_id=word.id, group_id=group.id)
                    db.add(word_group_link)
            
            db.commit()
            print(f"  ✅ {filename} processed into group '{group_name}'")
            
    except Exception as e:
        print(f"Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("Database seeding completed")


@task
def reset_db(c):
    """Complete database reset - drop, create, migrate, and seed"""
    print("Performing complete database reset...")
    
    # Drop all tables
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Initialize database
    init_db(c)
    
    # Run migrations
    migrate_db(c)
    
    # Seed study activities
    seed_study_activities(c)
    
    # Seed data
    seed_data(c)
    
    print("Database reset completed successfully")


@task
def create_dirs(c):
    """Create necessary directories for the project"""
    print("Creating project directories...")
    
    directories = ["migrations", "seeds"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")
    
    # Create sample migration file if migrations directory is empty
    migrations_dir = "migrations"
    if not os.listdir(migrations_dir):
        sample_migration = """-- 0001_init.sql
-- Initial database setup

-- This file can contain additional SQL commands
-- that need to be run during database initialization

-- Example: Create indexes
-- CREATE INDEX idx_words_korean ON words(korean);
-- CREATE INDEX idx_word_review_items_created_at ON word_review_items(created_at);
"""
        with open(os.path.join(migrations_dir, "0001_init.sql"), 'w') as f:
            f.write(sample_migration)
        print("Created sample migration file: 0001_init.sql")
    
    print("Directory creation completed")


@task
def check_db(c):
    """Check database status and show table info"""
    print("Checking database status...")
    
    db = SessionLocal()
    try:
        from models import Word, Group, StudySession, StudyActivity, WordReviewItem
        
        # Count records in each table
        word_count = db.query(Word).count()
        group_count = db.query(Group).count()
        session_count = db.query(StudySession).count()
        activity_count = db.query(StudyActivity).count()
        review_count = db.query(WordReviewItem).count()
        
        print("Database Status:")
        print(f"  Words: {word_count}")
        print(f"  Groups: {group_count}")
        print(f"  Study Sessions: {session_count}")
        print(f"  Study Activities: {activity_count}")
        print(f"  Word Reviews: {review_count}")
        
        # Check if tables exist
        tables_exist = True
        try:
            db.query(Word).first()
        except Exception as e:
            tables_exist = False
            print(f"\nWarning: Tables may not exist - {e}")
        
        if tables_exist:
            print("\n✅ Database is properly initialized")
        else:
            print("\n❌ Database needs initialization")
            
    except Exception as e:
        print(f"Error checking database: {e}")
    finally:
        db.close()


@task
def setup(c):
    """Complete project setup - create directories, init database, migrate, and seed"""
    print("Setting up project...")
    
    # Create directories
    create_dirs(c)
    
    # Initialize database
    init_db(c)
    
    # Run migrations
    migrate_db(c)
    
    # Seed study activities first
    seed_study_activities(c)
    
    # Seed data (if seed files exist)
    if os.path.exists("seeds") and os.listdir("seeds"):
        seed_data(c)
    else:
        print("No seed files found. Add JSON files to seeds/ directory and run 'invoke seed-data'")
    
    print("Project setup completed successfully!")
    print("\nNext steps:")
    print("1. Add JSON seed files to the seeds/ directory")
    print("2. Run 'invoke seed-data' to populate the database")
    print("3. Start the API server with 'uvicorn main:app --reload'")