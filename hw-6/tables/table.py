import sqlite3
import logging
from abc import abstractmethod


class Table:
    __connection: sqlite3.Connection = None

    def __init__(
        self, table_name: str, table_columns: dict, constraints: tuple[str, ...] = ()
    ):
        self.table_name = table_name

        cursor = self.connection.cursor()
        sql_fields = (", ").join(
            [f"{key} {value}" for key, value in table_columns.items()]
        )
        sql_constraints = (
            f", {(', ').join(constraints)}" if len(constraints) > 0 else ""
        )
        sql_script = (
            f"CREATE TABLE IF NOT EXISTS {table_name} ({sql_fields}{sql_constraints})"
        )

        logging.debug(f"__init__: {sql_script}")

        try:
            cursor.execute(sql_script)
            self.connection.commit()
        except sqlite3.Error as error:
            logging.error(error)
        finally:
            cursor.close()

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, connection: sqlite3.Connection):
        self.__connection = connection

    def insert(self, dictionary: dict):
        cursor = self.connection.cursor()

        values = f"({', '.join(['?'] * len(dictionary.keys()))})"
        sql_script = f"INSERT INTO {self.table_name} ({', '.join(dictionary.keys())}) VALUES {values}"

        logging.debug(f"insert: {dictionary}, {sql_script}")

        try:
            cursor.execute(sql_script, list(dictionary.values()))
            self.connection.commit()
        except sqlite3.Error as error:
            logging.error(error)
        finally:
            cursor.close()

    def select_all(self):
        cursor = self.connection.cursor()

        rows = None

        try:
            cursor.execute(f"SELECT * FROM {self.table_name};")
            rows = cursor.fetchall()
        except sqlite3.Error as error:
            logging.error(error)
        finally:
            cursor.close()

        logging.debug(f"select_all {rows}")

        return rows

    @abstractmethod
    def generate_data(self):
        raise NotImplementedError(
            f"You have to define method named generate_data in {type(self).__name__} class"
        )
