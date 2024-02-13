from .table import Table
from dataclasses import dataclass
import logging
import sqlite3
from get_sql_script import get_sql_script


@dataclass
class Group:
    name: str


class Groups(Table):
    def __init__(self):
        super().__init__(
            "groups",
            {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
                "name": "VARCHAR(30) UNIQUE NOT NULL",
                "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            },
        )

    def generate_data(self):
        self.insert(Group(name="Backend").__dict__)
        self.insert(Group(name="Frontend").__dict__)
        self.insert(Group(name="UI/UX").__dict__)

    def query_6(self, group_id: int):
        cursor = self.connection.cursor()

        rows = None

        try:
            cursor.execute(get_sql_script("query_6.sql"), (group_id, group_id))
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 6 {rows}")

        return rows

    def query_7(self, group_id: int, subject_id: int):
        cursor = self.connection.cursor()

        rows = None

        try:
            cursor.execute(
                get_sql_script("query_7.sql"),
                (group_id, subject_id, subject_id, group_id),
            )
            rows = cursor.fetchall()
        except (sqlite3.Error, OSError) as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"query 6 {rows}")

        return rows
