# Frontend Technical Specs

## Pages

### Dashboard `/dashboard`

#### Purpose
The purpose of this page is to provide a summary of learning
and act as the default page when a user visit the webapp

#### Components
This page contains the following components
- Last Study Session
    - shows last activity used
    - shows when last activity used
    - summarizes wrong vs correct from last activity
    - has a link to the group
- Study Progress
    - total words studied out of entire vocab
        - across all study session show the total words studied out of all possible words in our database
    - display a mastery progress
- Quick stats
    - success rate eg. 80%
    - total study sessions eg.4
    - total active groups eg.3
    - study streak eg. 4 days
- Start Studying Button
    - goes to study activities page

we'll need the following API endpoints to power this page

#### Needed API endpoints
- GET /api/dashboard/last_study_session
- GET /api/dashboard/study_progress
- GET /api/dashboard/quick_stats

### Study Activities Index `/study-activities`

#### Purpose
The purpose of this page is to show a collection of study activities
with a thumbnail and its name, to either launch or view the study activity.

#### Components
This page contains the following components

- Study Activity Card
    -  show a thumbnail of the study activity
    -  the name of the study activity
    -  a launch button to take us to the launchpage
    -  the view page to view more information about past study sessions for the study activity

#### Needed API endpoints
- GET /api/study_activities

### Study Activity Show `/study_activities/:id`

#### Purpose
The purpose of this page is to show the details of a study activity and its past study sessions

#### Components
- Name of study Activity
- Thumbnail of study Activity
- Description of study Activity
- Launch Button
- Study Activity Paginated List
    - id
    - activity name
    - group name
    - start time
    - end time (inferred by the last word_review_item submitted)
    - number of review items

#### Needed API endpoints
- GET /api/study_activities/:id
- GET /api/study_activities/:id/study_sessions

### Study Activity Launch `study_activities/:id/launch`

#### Purpose
The purpose of this page is to launch the study activity

#### Components
- Name of study activity 
- Launch form
    - select field for group
    - launch now button

## Behavior
After the form is submitted a new tab opens with the study activity based on its URL provided in the database

Also the after form is submittede thte page will redirect to the study session show page

#### Needed API endpoints
- POST /api/study_activities

### Words Index `/words`

#### Purpose
The purpose of this page is to show all words in our database

#### Components
- Paginated word list
    - Columns
        - Korean
        - Transliteration
        - English
        - Correct Count
        - Wrong Count
    - Pagination with 100 items per page
    - clicking on the Korean word will take us to the word show page

#### Needed API endpoints
- GET /api/words

### Word Show `/words/:id`

#### Purpose
The purpose of this pagea is to show information about a specific word

#### Components
- Korean
- Transliteration
- English
- Study Statistics
    - Correct Count
    - Wrong Count
- Word Groups
    - Shows a series of pills eg. tags
    - when group name is clicked it will take us to the group show page

#### Needed API endpoints
- GET /api/words/:id

### Words Groups Index `/groups`

#### Purpose
The purpose of this page is to show a list of groups in the database:

#### Components
- Paginated Group List
    - Columns
        -Group Name
        - Word Count
    - Clicking the group name will take us to the group show page

#### Needed API endpoints
- GET /api/groups

### Group Show `/groups/:id`

#### Purpose
The purpose of this page is to show information about a 
specific group

#### Components
- Group Name
- Group Statistics
    - Total Word Count
- Words in Group ( Paginateds List of Words)
    - Should use the same components as the words index page
- Study Sessions ( Paginated List of study sessions)
    - Should use the same component as the study sessions index page

#### Needed API endpoints
- GET /api/groups/:id (the name and groups stats)
- GET /api/groups/:id/words
- GET /api/groups/:id/study_sessions

### Study Sessions Index `/study_sessions`

#### Purpose
The Purpose of this page is to show a list of study sessions in our database

#### Components
- Paginated Study Session List
    - Columns
        - Id
        - Activity Name
        - Group Name
        - Start Time
        - End Time
        - Number of Review Items
    - Clicking the study session id will take us to the study session show page

#### Needed API endpoints
- GET /api/study_sessions

### Study Session Show `/study_session/:id`

#### Purpose
THe purpose fo this page is to show information about a specific study session

#### Components
- Study Session Details
    - Activity Name
    - Group Name
    - Start Time
    - End Time
    - Number of Review Items
- Words Review Items (Paginated List of words)
    - Should use the same component as the words index page

#### Needed API endpoints
- GET /api/study_session/:id
- GET /api/study_session/:id/words

### Settings Page `/settings`

#### Purpose
The purpose of this page is to make configuration to the study portal

#### Components
- Theme Selection eg. Light, Dark, System Default
- Reset History Button
    - this will delete all study sessions and word review items
- Full Reset Button
    - this will drop all tables and re-creates with seed data

#### Needed API endpoints
- POST /api/reset/history
- POST /api/full_reset