"""
Student data model — plain Python object from a database row.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Student:
    id: int
    username: str
    password_hash: str
    join_date: date
    expiry_date: date
    is_active: bool

    @classmethod
    def from_row(cls, row) -> "Student":
        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            join_date=date.fromisoformat(row["join_date"]),
            expiry_date=date.fromisoformat(row["expiry_date"]),
            is_active=bool(row["is_active"]),
        )
