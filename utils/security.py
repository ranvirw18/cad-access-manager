"""
Password hashing with bcrypt — never store plain-text passwords.
"""

import bcrypt


def hash_password(plain_password: str) -> str:
    """Convert password to a safe string for SQLite storage."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Return True if password matches the stored hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )
