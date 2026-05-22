"""
Admin authentication and student management.
"""

from datetime import date

from models.admin import Admin
from repositories.admin_repository import AdminRepository
from repositories.student_repository import StudentRepository
from utils.security import verify_password


class AdminService:
    def __init__(
        self,
        admin_repo: AdminRepository | None = None,
        student_repo: StudentRepository | None = None,
    ):
        self._admins = admin_repo or AdminRepository()
        self._students = student_repo or StudentRepository()

    def login_admin(self, username: str, password: str) -> Admin | None:
        admin = self._admins.get_by_username(username)
        if not admin:
            return None
        if not verify_password(password, admin.password_hash):
            return None
        return admin

    def list_students(self):
        return self._students.list_all()

    def add_student(self, username: str, password: str, join_date: date | None = None):
        return self._students.add(username, password, join_date)

    def remove_student(self, student_id: int):
        self._students.remove(student_id)

    def change_password(self, student_id: int, new_password: str):
        self._students.set_password(student_id, new_password)

    def set_account_active(self, student_id: int, active: bool):
        self._students.set_active(student_id, active)

    def extend_validity(self, student_id: int, extra_days: int):
        self._students.extend_days(student_id, extra_days)
