"""
Login validation — all business rules in one place for the student UI.
"""

from dataclasses import dataclass
from enum import Enum

from models.student import Student
from repositories.student_repository import StudentRepository
from utils.dates import is_expired
from utils.security import verify_password


class LoginStatus(Enum):
    SUCCESS = "success"
    USER_NOT_FOUND = "user_not_found"
    WRONG_PASSWORD = "wrong_password"
    ACCOUNT_DISABLED = "account_disabled"
    SUBSCRIPTION_EXPIRED = "subscription_expired"


@dataclass
class LoginResult:
    status: LoginStatus
    student: Student | None = None

    @property
    def ok(self) -> bool:
        return self.status == LoginStatus.SUCCESS


class AuthService:
    def __init__(self, student_repo: StudentRepository | None = None):
        self._students = student_repo or StudentRepository()

    def login_student(self, username: str, password: str) -> LoginResult:
        student = self._students.get_by_username(username)
        if not student:
            return LoginResult(LoginStatus.USER_NOT_FOUND)

        if not verify_password(password, student.password_hash):
            return LoginResult(LoginStatus.WRONG_PASSWORD)

        if not student.is_active:
            return LoginResult(LoginStatus.ACCOUNT_DISABLED)

        if is_expired(student.expiry_date):
            return LoginResult(LoginStatus.SUBSCRIPTION_EXPIRED, student=student)

        return LoginResult(LoginStatus.SUCCESS, student=student)
