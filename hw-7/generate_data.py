from models import Group, Subject, Teacher, Grade, Student
from faker import Faker
from random import randint, seed
from db import session


def generate_data():
    fake = Faker()
    seed()

    groups = []

    for group_name in ("Frontend", "Backend", "Devops"):
        group = Group(name=group_name)
        groups.append(group)
        session.add(group)

    students = []
    students_count = 40

    for i in range(students_count):
        student = Student(name=fake.name(), group_id=randint(1, len(groups)))
        students.append(student)
        session.add(student)

    teachers = []
    teachers_count = 5

    for i in range(teachers_count):
        teacher = Teacher(name=fake.name())
        teachers.append(teacher)
        session.add(teacher)

    subjects = []

    for subject_name in (
        "HTML5/CSS3",
        "REACT",
        "TYPESCRIPT",
        "DATABASES",
        "HTTPS",
        "SOLID",
        "AWS",
        "DOCKER",
    ):
        subject = Subject(
            name=subject_name, teacher=teachers[randint(0, teachers_count - 1)]
        )
        subjects.append(subject)
        session.add(subject)

    first_datetime = fake.date_time()
    second_datetime = fake.date_time()

    first_lesson_datetime, second_lesson_datetime = (
        (first_datetime, second_datetime)
        if first_datetime < second_datetime
        else (second_datetime, first_datetime)
    )

    for student in students:
        for subject in subjects:
            grade1 = Grade(
                subject=subject,
                student=student,
                teacher=teachers[randint(0, teachers_count - 1)],
                value=randint(1, 12),
                created_at=first_lesson_datetime,
            )
            grade2 = Grade(
                subject=subject,
                student=student,
                teacher=teachers[randint(0, teachers_count - 1)],
                value=randint(1, 12),
                created_at=second_lesson_datetime,
            )

            session.add(grade1)
            session.add(grade2)

    session.commit()
