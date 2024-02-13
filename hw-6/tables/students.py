from .table import Table
from dataclasses import dataclass
from random import randint, seed
from faker import Faker
import sqlite3
import logging
from get_sql_script import get_sql_script


@dataclass
class Student:
    group_id: int
    name: str


class Students(Table):
    def __init__(self):
        super().__init__(
            "students",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "group_id": "INTEGER NOT NULL",
                "name": "VARCHAR(30) NOT NULL",
                "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
            ("FOREIGN KEY (group_id) REFERENCES groups (id)",),
        )

    def generate_data(self):
        seed()

        fake = Faker()

        for i in range(31):
            self.insert(Student(group_id=randint(1, 3), name=fake.name()).__dict__)

    def query_1(self):
        cursor = self.connection.cursor()

        rows = None

        try:
            cursor.execute(get_sql_script("query_1.sql"))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 1 {rows}")

        return rows

    def query_2(self, subject_id: int):
        cursor = self.connection.cursor()
        student = None

        try:
            cursor.execute(get_sql_script("query_2.sql"), (subject_id,))
            student = cursor.fetchone()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 2 {student}")

        return student

    def query_9(self, student_id: int):
        cursor = self.connection.cursor()
        rows = None

        try:
            cursor.execute(get_sql_script("query_9.sql"), (student_id,))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 9 {rows}")

        return rows

    def query_10(self, student_id: int, teacher_id: int):
        cursor = self.connection.cursor()
        rows = None

        try:
            cursor.execute(get_sql_script("query_10.sql"), (student_id, teacher_id))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 10 {rows}")

        return rows
