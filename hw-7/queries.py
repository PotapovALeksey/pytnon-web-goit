from sqlalchemy import desc, func, and_, select
from db import session
from models import Grade, Student, Subject, Group, Teacher
from decoratos import query_logger, query_exception_handler


@query_logger(1)
@query_exception_handler
def query_1():
    average_grade = func.round(func.avg(Grade.value), 2).label("avg_grade")

    return (
        session.query(Student.name, average_grade)
        .select_from(Grade)
        .join(Student)
        .group_by(Grade.student_id)
        .order_by(desc(average_grade))
        .limit(5)
        .all()
    )


@query_logger(2)
@query_exception_handler
def query_2(subject_id: int):
    average_grade = func.avg(Grade.value).label("avg_grade")

    return (
        session.query(Subject.name, Student.name, average_grade)
        .select_from(Grade)
        .where(Grade.subject_id == subject_id)
        .join(Student)
        .join(Subject)
        .group_by(Grade.student_id)
        .order_by(desc(average_grade))
        .first()
    )


@query_logger(3)
@query_exception_handler
def query_3(subject_id: int):
    return (
        session.query(
            Group.name,
            Subject.name,
            func.round(func.avg(Grade.value), 2).label("avg_grade"),
        )
        .where(Grade.subject_id == subject_id)
        .join(Subject)
        .join(Student)
        .join(Group)
        .group_by(Group.name)
        .order_by(desc("avg_grade"))
        .all()
    )


@query_logger(4)
@query_exception_handler
def query_4():
    return session.query(func.round(func.avg(Grade.value), 2)).one()


@query_logger(5)
@query_exception_handler
def query_5(teacher_id: int):
    teacher = session.query(Teacher).where(Teacher.id == teacher_id).one()

    return (teacher.name, [subject.name for subject in teacher.subjects])


@query_logger(6)
@query_exception_handler
def query_6(group_id: int):
    group = session.query(Group).where(Group.id == group_id).one()
    return (group.name, [student.name for student in group.students])


@query_logger(7)
@query_exception_handler
def query_7(group_id: int, subject_id: int):
    return (
        session.query(Group.name, Subject.name, Student.name, Grade.value)
        .select_from(Student)
        .where(Student.group_id == group_id)
        .join(Grade, Grade.student_id == Student.id)
        .where(Grade.subject_id == subject_id)
        .join(Group, Group.id == group_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .all()
    )


@query_logger(8)
@query_exception_handler
def query_8(teacher_id: int):
    return (
        session.query(Teacher.name, Subject.name, func.round(func.avg(Grade.value), 2))
        .select_from(Grade)
        .where(Grade.teacher_id == teacher_id)
        .join(Teacher, Teacher.id == teacher_id)
        .join(Subject, Subject.teacher_id == teacher_id)
        .group_by(Subject.name)
        .all()
    )


@query_logger(9)
@query_exception_handler
def query_9(student_id: int):
    return (
        session.query(Student.name, Subject.name)
        .select_from(Grade)
        .where(Grade.student_id == student_id)
        .join(Student, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .group_by(Subject.name)
        .all()
    )


@query_logger(10)
@query_exception_handler
def query_10(student_id: int, teacher_id: int):
    return (
        session.query(Teacher.name, Subject.name, Student.name)
        .select_from(Grade)
        .filter(and_(Grade.student_id == student_id, Grade.teacher_id == teacher_id))
        .join(Student, Student.id == Grade.student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .join(Teacher, Teacher.id == Grade.teacher_id)
        .group_by(Subject.name)
        .all()
    )


@query_logger(11)
@query_exception_handler
def query_11(student_id: int, teacher_id: int):
    return (
        session.query(
            Teacher.name,
            Subject.name,
            Student.name,
            func.round(func.avg(Grade.value), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .filter(and_(Grade.student_id == student_id, Grade.teacher_id == teacher_id))
        .join(Teacher, Teacher.id == teacher_id)
        .join(Student, Student.id == student_id)
        .join(Subject, Subject.id == Grade.subject_id)
        .group_by(Subject.name)
        .all()
    )


@query_logger(12)
@query_exception_handler
def query_12(group_id: int, subject_id: int):
    subquery = (
        select(func.max(Grade.created_at))
        .join(Student)
        .join(Group)
        .filter(and_(Group.id == group_id, Grade.subject_id == subject_id))
        .scalar_subquery()
    )

    return (
        session.query(
            Group.name, Student.name, Subject.name, Grade.value, Grade.created_at
        )
        .select_from(Grade)
        .join(Subject)
        .join(Student)
        .join(Group)
        .filter(
            and_(
                Group.id == group_id,
                Subject.id == subject_id,
                Grade.created_at == subquery,
            )
        )
        # .group_by(Student.name)
        .all()
    )
