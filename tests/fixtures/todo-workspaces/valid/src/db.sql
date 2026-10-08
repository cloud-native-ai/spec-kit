-- Users table anchors all account data
-- Email lookups are the hot path
-- SPECKIT TODO
-- Add soft-delete support:
-- - Add deleted_at column
-- - Update active queries to filter soft-deleted rows
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL
);
