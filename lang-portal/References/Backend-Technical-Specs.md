# Backend Server Technical Specs

## Business Goal:

A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a record store, providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps


## Technical Requirements

- The backend will be built using Go
- The database will be SQLite3
- The API will be built using Gin
- The API will always return JSON
- There will be no authentication or authorization 
- Everything will be treated as a single user

## Database Schema

We have the following tables:
- words - stored vocabulary words
    - id integer
    - korean string
    - transliteration string
    - english string
    - parts json
- words_groups - join table for words and groups many-to-many
    - id integer
    - word_id integer
    - group_id integer
- groups - thematic groups of words
    - id integer
    - name string
- study_session - records of study sessions grouping word_review_items
    - id integer
    - group_id integer
    - study_activity_id integer
    - created_at datetime
- study_activities - a specific study activity, linking a study session to group
    - id integer
    - study_session_id integer
    - group_id integer
    - created_at datetime
- word_review_items - a record of word practice, determining if the word was correct or not
    - word_id integer
    - study_session_id integer
    - correct boolean
    - created_at datetime

## API Endpoints

- GET /api/words
      - pagination with 100 words per page
- GET /api/words/:id
- GET /api/groups
    - pagination with 100 words per page
- GET /api/groups/:id (the name and groups stats)
- GET /api/groups/:id/words
- GET /api/study_activities/:id
- GET /api/study_activities/:id/study_sessions
- GET /api/dashboard/last_study_session
- GET /api/dashboard/study_progress
- GET /api/dashboard/quick_stats
- POST /api/study_activities
      -requires params:group_id, study_activity_id
- GET /api/groups/:id/study_sessions
- GET /api/study_sessions  
- GET /api/study_session/:id
- GET /api/study_session/:id/words
- POST /api/reset/history
- POST /api/full_reset
- POST /api/study_sessions/:id/words/:word_id/review