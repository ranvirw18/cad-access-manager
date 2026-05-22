from database.connection import get_connection
from models.admin import Admin


class AdminRepository:
    def get_by_username(self, username: str) -> Admin | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM admins WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
        conn.close()
        return Admin.from_row(row) if row else None
