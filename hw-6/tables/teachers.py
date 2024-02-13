from .table import Table
from dataclasses import dataclass
from random import randint, seed
from faker import Faker
import logging
import sqlite3
from get_sql_script import get_sql_script


@dataclass
class Teacher:
    name: str
    group_id: int


class Teachers(Table):
    def __init__(self):
        super().__init__(
            "teachers",
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

        for i in range(5):
            self.insert(Teacher(group_id=randint(1, 3), name=fake.name()).__dict__)

    def query_5(self, subject_id: int):
        cursor = self.connection.cursor()

        rows = None

        try:
            cursor.execute(get_sql_script("query_5.sql"), (subject_id, subject_id))
            rows = cursor.fetchall()
        except sqlite3.Error as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 5 {rows}")

        return rows

    def query_8(self, teacher_id: int):
        cursor = self.connection.cursor()

        rows = None

        try:
            cursor.execute(get_sql_script("query_8.sql"), (teacher_id,))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 8 {rows}")

        return rows
