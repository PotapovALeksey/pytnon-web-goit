import sqlite3
from tables.table import Table
from tables.groups import Groups
from tables.students import Students
from tables.teachers import Teachers
from tables.subjects import Subjects
from tables.grades import Grades
import logging

logging.basicConfig(format="line_num: %(lineno)s > %(message)s", level=logging.DEBUG)


if __name__ == "__main__":
    with sqlite3.connect("db") as connection:
        Table.connection = connection

        groups = Groups()
        students = Students()
        teachers = Teachers()
        grades = Grades()
        subjects = Subjects()

        students.query_1()
        # students.query_2(3)
        # grades.query_3(3)
        # grades.query_4()
        # teachers.query_5(3)
        # groups.query_6(2)
        # groups.query_7(2, 1)
        # teachers.query_8(1)
        # students.query_9(2)
        # students.query_10(2, 3)

        # groups.generate_data()
        # students.generate_data()
        # teachers.generate_data()
        # subjects.generate_data()
        # grades.generate_data()
