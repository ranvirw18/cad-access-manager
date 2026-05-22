"""
Database connection — one place to open SQLite and run migrations.
"""

import sqlite3
from pathlib import Path

from config.settings import (
    DATABASE_PATH,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_USERNAME,
)
from utils.security import hash_password


def get_connection() -> sqlite3.Connection:
    """Open database; create data folder and tables if needed."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _init_schema(conn)
    _seed_default_admin(conn)
    return conn


def _init_schema(conn: sqlite3.Connection) -> None:
    schema_path = Path(__file__).parent / "schema.sql"
    conn.executescript(schema_path.read_text(encoding="utf-8"))
    conn.commit()


def _seed_default_admin(conn: sqlite3.Connection) -> None:
    """Create default admin only when no admins exist."""
    row = conn.execute("SELECT COUNT(*) AS c FROM admins").fetchone()
    if row["c"] > 0:
        return
    conn.execute(
        "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
        (DEFAULT_ADMIN_USERNAME, hash_password(DEFAULT_ADMIN_PASSWORD)),
    )
    conn.commit()
