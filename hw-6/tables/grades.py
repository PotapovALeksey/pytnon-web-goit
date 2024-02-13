from .table import Table
from dataclasses import dataclass
from random import randint, seed
import logging
import sqlite3
from get_sql_script import get_sql_script


@dataclass
class Grade:
    subject_id: int
    student_id: int
    teacher_id: int
    value: int


class Grades(Table):
    def __init__(self):
        super().__init__(
            "grades",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "subject_id": "INTEGER NOT NULL",
                "student_id": "INTEGER NOT NULL",
                "teacher_id": "INTEGER NOT NULL",
                "value": "TINY INTEGER",
                "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            (
                "FOREIGN KEY (subject_id) REFERENCES subjects (id)",
                "FOREIGN KEY (student_id) REFERENCES students (id)",
                "FOREIGN KEY (teacher_id) REFERENCES teachers (id)",
            ),
        )

    def generate_data(self):
        seed()

        students_count = 31
        subjects_count = 8

        for _ in range(6):
            for student_id in range(1, students_count + 1):
                for subject_id in range(1, subjects_count + 1):
                    self.insert(
                        Grade(
                            subject_id=subject_id,
                            student_id=student_id,
                            teacher_id=randint(1, 5),
                            value=randint(1, 12),
                        ).__dict__
                    )

    def query_3(self, subject_id: int):
        cursor = self.connection.cursor()
        rows = None

        try:
            cursor.execute(get_sql_script("query_3.sql"), (subject_id,))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 3 {rows}")

        return rows

    def query_4(self):
        cursor = self.connection.cursor()
        rows = None

        try:
            cursor.execute(get_sql_script("query_4.sql"))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 4 {rows}")

        return rows
