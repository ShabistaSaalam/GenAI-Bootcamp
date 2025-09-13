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

Our Database will be a single sqlite database called `words.db`
that will be in the root of the project folder of `backend-FastAPI`

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

### GET /api/words
- pagination with 100 words per page
#### JSON Response
```json
{
  "items": [
    {
      "korean": "안녕하세요",
      "transliteration": "annyeonghaseyo",
      "english": "hello",
      "correct_count": 11,
      "wrong_count": 1
    }
  ],
  "pagination":{
        "current_page":1,
        "total_pages":5,
        "total_items":500,
        "items_per_page":100
    }
}
```

### GET /api/words/:id
#### JSON Response
```json
{
  "korean": "안녕하세요", 
  "transliteration": "annyeonghaseyo",
  "english": "hello",
  "stats":{
  "correct_count": 11,
  "wrong_count": 1
  },
  "groups": [
    {
      "id": 1,
      "name": "Basic Greetings"
    },
    {
      "id": 5, 
      "name": "Daily Conversations"
    }
  ]
}
```

### GET /api/groups
- pagination with 20 items per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Basic Greetings",
      "word_count": 20
    }
  ],
  "pagination":{
        "current_page":1,
        "total_pages":1,
        "total_items":10,
        "items_per_page":100
    }
}
```

### GET /api/groups/:id (the name and groups stats)
#### JSON Response
```json
{
  "id": 1,
  "name": "Basic Greetings",
  "stats":{
    "total_word_count": 20
  }
}
```

### GET /api/groups/:id/words
#### JSON Response
```json
{
  "items": [
    {
      "korean": "안녕하세요",
      "transliteration": "annyeonghaseyo", 
      "english": "hello",
      "correct_count": 11,
      "wrong_count": 1
    }
  ],
   "pagination":{
        "current_page":1,
        "total_pages":5,
        "total_items":20,
        "items_per_page":100
    }
}
```
### GET /api/groups/:id/study_sessions
#### JSON Response
```json
{
  "items": [
    {
      "id": 3,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-09-11T09:15:00Z", 
      "end_time": "2025-09-11T09:30:00Z",
      "review_items_count": 12
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 20
  }
}
```
### GET /api/study_activities/:id
#### JSON Response
```json
{
  "id": 1,
  "name": "Vocabulary Quiz",
  "thumbnail": "/thumbnails/flashcards.png",
  "description": "Practice vocabulary with digital flash cards",
  "url": "https://flashcards.app/launch"
}
```

### GET /api/study_activities/:id/study_sessions
- pagination with 20 words per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 5,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Food & Dining", 
      "start_time": "2025-09-12T14:30:00Z",
      "end_time": "2025-09-12T14:45:00Z",
      "review_items_count": 10
    }
  ],
    "pagination":{
        "current_page":1,
        "total_pages":5,
        "total_items":100,
        "items_per_page":20
    }
}
```

### GET /api/dashboard/last_study_session
#### JSON Response
```json
{
    "id": 123,
    "group_id": 456,
    "study_activity_id": 231,
    "group_name":"Basic Greetings",
    "created_at": "2025-09-12T15:45:00Z"
}
```

### GET /api/dashboard/study_progress
Returns study progress statistics.
Please note that the frontend will determine progress bar based on total words studied and total available words
#### JSON Response
```json
{
  "total_words_studied": 45,
  "total_available_words": 350
}
```

### GET /api/dashboard/quick_stats
Returns quick overview statistics
#### JSON Response
```json
{
  "success_rate": 80.5,
  "total_study_sessions": 4,
  "total_active_groups": 3,
  "study_streak_days": 4
}
```

### GET /api/study_activities
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Vocabulary Quiz",
      "thumbnail": "/thumbnails/flashcards.png",
      "url": "https://flashcards.app/launch"
    }
  ]
}
```
### POST /api/study_activities
#### Request Params
- group_id integer,
- study_activity_id integer
#### JSON Response
```json
{
  "id": 122,
  "group_id": 2
}
```


### GET /api/study_sessions 
#### JSON Response
```json
{
  "items": [
    {
      "id": 6,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Food & Dining",
      "start_time": "2025-09-12T15:45:00Z",
      "end_time": "2025-09-12T16:00:00Z", 
      "review_items_count": 10
    }
  ],
  "pagination":{
        "current_page":1,
        "total_pages":5,
        "total_items":100,
        "items_per_page":100
    }
}
``` 
### GET /api/study_session/:id
- Pagination with 100 items per page
#### JSON Response
```json
{
  "id": 6,
  "activity_name": "Vocabulary Quiz", 
  "group_name": "Food & Dining",
  "start_time": "2025-09-12T15:45:00Z",
  "end_time": "2025-09-12T16:00:00Z",
  "review_items_count": 20
}
```

### GET /api/study_session/:id/words
#### JSON Response
```json
{
  "items": [
    {
      "korean": "김치",
      "transliteration": "gimchi", 
      "english": "kimchi",
      "correct_count": 5,
      "wrong_count":3
    }
  ],
  "pagination":{
        "current_page":1,
        "total_pages":5,
        "total_items":20,
        "items_per_page":100
    }
}
```

### POST /api/reset/history
#### JSON Response
```json
{
  "success": true,
  "message": "Study history reset successfully"
}
```

### POST /api/full_reset
#### JSON Response
```json
{
  "success": true,
  "message": "Full reset completed successfully"
}
```

### POST /api/study_sessions/:id/words/:word_id/review
#### Request Params
- id (study_session_id) integer
- word_id integer
- correct boolean
#### Request Payload
```json
{
  "correct": true
}
```

#### JSON Response
```json
{
  "success":true,
  "word_id": 15,
  "study_session_id": 6,
  "correct": true,
  "created_at": "2025-09-13T10:30:00Z"
}
```

## Invoke Tasks
Invoke is a task runner for Python.
Let's list out possible tasks we need for our language portal.

### Initialize Database
This task wil initialize the sqlite database called `words.db`

### Migrate Database
This task will run a series of migration sql files on the database

Migration Live in the `migration` folder
The Migration files will be run in order of their file name
The file name should look like this

```sql
0001_init.sql
0002_create_words_table.sql
```

### Seed Data
This task will import json files and transform them into target data for our database

All seed files live in the `seeds` folder.
All seed files should be loaded.

In our task we should have DSL(Domain Specific Language) to specific each seed file and its expected group word name

```json
[
  {
  "korean": "먹다",
  "transliteration": "meokda",
  "english": "to eat"
}
]
```