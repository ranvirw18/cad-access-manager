from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    username: str
    password_hash: str

    @classmethod
    def from_row(cls, row) -> "Admin":
        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
        )
