"""
Student database operations — UI and services talk to this, not raw SQL.
"""

from datetime import date, timedelta

from database.connection import get_connection
from models.student import Student
from utils.dates import expiry_from_join
from utils.security import hash_password


class StudentRepository:
    def get_by_username(self, username: str) -> Student | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM students WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
        conn.close()
        return Student.from_row(row) if row else None

    def list_all(self) -> list[Student]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM students ORDER BY username COLLATE NOCASE"
        ).fetchall()
        conn.close()
        return [Student.from_row(r) for r in rows]

    def add(self, username: str, plain_password: str, join_date: date | None = None) -> Student:
        join = join_date or date.today()
        expiry = expiry_from_join(join)
        conn = get_connection()
        try:
            conn.execute(
                """
                INSERT INTO students (username, password_hash, join_date, expiry_date, is_active)
                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    username.strip().lower(),
                    hash_password(plain_password),
                    join.isoformat(),
                    expiry.isoformat(),
                ),
            )
            conn.commit()
        except Exception:
            conn.close()
            raise
        student = self.get_by_username(username)
        conn.close()
        if not student:
            raise RuntimeError("Failed to create student")
        return student

    def remove(self, student_id: int) -> None:
        conn = get_connection()
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

    def set_password(self, student_id: int, plain_password: str) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE students SET password_hash = ?, updated_at = datetime('now') WHERE id = ?",
            (hash_password(plain_password), student_id),
        )
        conn.commit()
        conn.close()

    def set_active(self, student_id: int, is_active: bool) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE students SET is_active = ?, updated_at = datetime('now') WHERE id = ?",
            (1 if is_active else 0, student_id),
        )
        conn.commit()
        conn.close()

    def extend_days(self, student_id: int, extra_days: int) -> None:
        """Add more days to expiry (admin 'extend validity')."""
        conn = get_connection()
        row = conn.execute(
            "SELECT expiry_date FROM students WHERE id = ?", (student_id,)
        ).fetchone()
        if not row:
            conn.close()
            raise ValueError("Student not found")
        current = date.fromisoformat(row["expiry_date"])
        new_expiry = current + timedelta(days=extra_days)
        conn.execute(
            "UPDATE students SET expiry_date = ?, updated_at = datetime('now') WHERE id = ?",
            (new_expiry.isoformat(), student_id),
        )
        conn.commit()
        conn.close()
