-- Additional table constraints and data setup

-- Add any additional constraints that weren't handled by SQLAlchemy
-- This file can be used for custom SQL that needs to run after table creation

-- Example: Add check constraints
-- ALTER TABLE word_review_items ADD CONSTRAINT check_created_at_not_null CHECK (created_at IS NOT NULL);

-- Example: Create views for common queries
CREATE VIEW IF NOT EXISTS word_stats AS
SELECT 
    w.id,
    w.korean,
    w.transliteration,
    w.english,
    COUNT(CASE WHEN wri.correct = 1 THEN 1 END) as correct_count,
    COUNT(CASE WHEN wri.correct = 0 THEN 1 END) as wrong_count
FROM words w
LEFT JOIN word_review_items wri ON w.id = wri.word_id
GROUP BY w.id, w.korean, w.transliteration, w.english;

-- Create view for group word counts
CREATE VIEW IF NOT EXISTS group_word_counts AS
SELECT 
    g.id,
    g.name,
    COUNT(wg.word_id) as word_count
FROM groups g
LEFT JOIN words_groups wg ON g.id = wg.group_id
GROUP BY g.id, g.name;

-- Create view for session statistics
CREATE VIEW IF NOT EXISTS session_stats AS
SELECT 
    ss.id,
    ss.group_id,
    ss.study_activity_id,
    ss.created_at,
    COUNT(wri.word_id) as review_items_count,
    COUNT(CASE WHEN wri.correct = 1 THEN 1 END) as correct_items,
    COUNT(CASE WHEN wri.correct = 0 THEN 1 END) as wrong_items
FROM study_sessions ss
LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
GROUP BY ss.id, ss.group_id, ss.study_activity_id, ss.created_at;