"""
Optional helper: create a test student from the command line.

  python scripts/seed_test_student.py rahul pass123
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from repositories.student_repository import StudentRepository


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/seed_test_student.py <username> <password>")
        sys.exit(1)
    repo = StudentRepository()
    s = repo.add(sys.argv[1], sys.argv[2])
    print(f"Created: {s.username} | expires {s.expiry_date}")


if __name__ == "__main__":
    main()
