-- Initial database setup and indexes

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_words_korean ON words(korean);
CREATE INDEX IF NOT EXISTS idx_words_english ON words(english);
CREATE INDEX IF NOT EXISTS idx_words_transliteration ON words(transliteration);

-- Create indexes for join tables
CREATE INDEX IF NOT EXISTS idx_words_groups_word_id ON words_groups(word_id);
CREATE INDEX IF NOT EXISTS idx_words_groups_group_id ON words_groups(group_id);

-- Create indexes for study sessions
CREATE INDEX IF NOT EXISTS idx_study_sessions_group_id ON study_sessions(group_id);
CREATE INDEX IF NOT EXISTS idx_study_sessions_study_activity_id ON study_sessions(study_activity_id);
CREATE INDEX IF NOT EXISTS idx_study_sessions_created_at ON study_sessions(created_at);

-- Create indexes for study activities
CREATE INDEX IF NOT EXISTS idx_study_activities_study_session_id ON study_activities(study_session_id);
CREATE INDEX IF NOT EXISTS idx_study_activities_group_id ON study_activities(group_id);
CREATE INDEX IF NOT EXISTS idx_study_activities_created_at ON study_activities(created_at);

-- Create indexes for word review items
CREATE INDEX IF NOT EXISTS idx_word_review_items_word_id ON word_review_items(word_id);
CREATE INDEX IF NOT EXISTS idx_word_review_items_study_session_id ON word_review_items(study_session_id);
CREATE INDEX IF NOT EXISTS idx_word_review_items_created_at ON word_review_items(created_at);
CREATE INDEX IF NOT EXISTS idx_word_review_items_correct ON word_review_items(correct);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_word_review_items_word_correct ON word_review_items(word_id, correct);
CREATE INDEX IF NOT EXISTS idx_study_sessions_group_activity ON study_sessions(group_id, study_activity_id);