import typing
import sqlite3
import logging

column_name = str
column_type = str


class Table:
    conn: sqlite3.Connection = None

    def __init__(
        self,
        table_name: str,
        columns: dict[column_name, column_type],
        constrains: list[str],
    ) -> None:
        self.colums = columns
        self.table_name = table_name
        self.constrains = constrains

        full_columns = [f"{key} {val}" for key, val in columns.items()]
        full_columns.extend(constrains)

        temp = (", ").join(full_columns)

        sql_request = f"CREATE TABLE IF NOT EXISTS {table_name} ({temp});"

        logging.debug(sql_request)

        try:
            c = self.conn.cursor()
            c.execute(sql_request)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            c.close()

    def create(self, obj_dict: dict) -> int | None:
        table_columns = (",").join(self.colums.keys())
        table_questions = (",").join("?" for _ in self.colums.keys())

        sql_request = (
            f"INSERT INTO {self.table_name}({table_columns}) VALUES({table_questions});"
        )

        logging.debug(sql_request)

        cur = self.conn.cursor()

        try:
            cur.execute(sql_request, list(obj_dict.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            cur.close()

        return cur.lastrowid

    def get_all(self) -> list[typing.Iterable[typing.Any]] | None:
        rows = None
        cur = self.conn.cursor()

        try:
            cur.execute(f"SELECT * FROM {self.table_name}")
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            cur.close()

        return rows

    def update(
        self, obj_dict: dict[str, typing.Any], where_fields: dict[str, typing.Any]
    ):
        obj_str = ", ".join(
            [f"{key} = ?" for key, value in obj_dict.items() if value is not None]
        )

        where_str = ", ".join([f"{i} = ?" for i in where_fields.keys()])

        sql = f"UPDATE {self.table_name} SET {obj_str} WHERE {where_str}"

        logging.debug(sql)

        parameters = [val for val in obj_dict.values() if val is not None]
        parameters.extend(list(where_fields.values()))

        cur = self.conn.cursor()
        try:
            cur.execute(sql, parameters)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            cur.close()

    def remove(self, where_fields: dict[str, typing.Any]):
        where_str = ", ".join([f"{i} = ?" for i in where_fields.keys()])
        parameters = list(where_fields.values())

        sql = f"DELETE FROM {self.table_name} WHERE {where_str}"

        logging.debug(sql)

        cur = self.conn.cursor()
        try:
            cur.execute(sql, parameters)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            cur.close()
