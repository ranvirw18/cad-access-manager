-- CAD Institute Launcher — SQLite schema
-- Run via database/connection.py on startup

CREATE TABLE IF NOT EXISTS students (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash   TEXT NOT NULL,
    join_date       TEXT NOT NULL,   -- ISO date: YYYY-MM-DD
    expiry_date     TEXT NOT NULL,   -- join_date + 50 days
    is_active       INTEGER NOT NULL DEFAULT 1,  -- 1 = active, 0 = disabled
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_students_username ON students(username);
CREATE INDEX IF NOT EXISTS idx_students_expiry ON students(expiry_date);

-- Admins are separate from students (admin never launches AutoCAD from student login)
CREATE TABLE IF NOT EXISTS admins (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash   TEXT NOT NULL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
