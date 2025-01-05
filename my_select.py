from connect import session
from models import (
    Student,
    Group,
    Subject,
    Teacher,
    Mark,
    groups_m2m_students,
    students_m2m_subjects
)
from sqlalchemy import and_, func
from tabulate import tabulate

OKGREEN = "\033[92m"
ENDC = "\033[0m"

def execute_query(query, headers, title):
    """
    Executes a query, formats the result as a table, and prints it.
    """
    print(OKGREEN + title + ENDC)
    table_data = [tuple(row) for row in query]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def select_1():
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")
    query = (
        session.query(Mark.student_id, Student.name, avg_mark)
        .join(Student, Mark.student_id == Student.id)
        .group_by(Mark.student_id, Student.name)
        .order_by(avg_mark.desc())
        .limit(5)
        .all()
    )
    execute_query(query, ["Student ID", "Student Name", "Average Mark"], "Task 1: Top-5 students with the highest average mark")


def select_2(subject_name="English"):
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")
    query = (
        session.query(Mark.student_id, Student.name, Subject.name, avg_mark)
        .join(Student, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Mark.student_id, Student.name, Subject.name)
        .order_by(avg_mark.desc())
        .first()
    )
    execute_query([query], ["Student ID", "Student Name", "Subject", "Average Mark"], f"Task 2: Student with the highest average mark for {subject_name}")


def select_3(subject_name="English"):
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")
    query = (
        session.query(Group.name, Subject.name, avg_mark)
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .join(Mark, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name, Subject.name)
        .all()
    )
    execute_query(query, ["Group Name", "Subject", "Average Mark"], f"Task 3: Average mark in each group for {subject_name}")


def select_4():
    avg_mark = func.round(func.avg(Mark.mark), 2).label("average_mark")
    query = session.query(avg_mark).scalar()
    print(f"{OKGREEN}Task 4: Average mark: {query}{ENDC}")


def select_5():
    query = (
        session.query(
            Teacher.name, func.string_agg(Subject.name, ", ").label("subjects")
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .group_by(Teacher.id)
        .all()
    )
    execute_query(query, ["Teacher Name", "Subjects"], "Task 5: Which subjects a particular teacher teaches")


def select_6():
    query = (
        session.query(Group.name, func.string_agg(Student.name, ", ").label("students"))
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .group_by(Group.name)
        .all()
    )
    execute_query(query, ["Group Name", "Students"], "Task 6: Students list for each group")


def select_7(subject_name="English"):
    query = (
        session.query(
            Group.name,
            Student.name,
            Subject.name,
            func.array_agg(Mark.mark).label("marks"),
        )
        .join(groups_m2m_students, Group.id == groups_m2m_students.c.group_id)
        .join(Student, groups_m2m_students.c.student_id == Student.id)
        .join(Mark, Mark.student_id == Student.id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name, Student.name, Subject.name)
        .all()
    )
    execute_query(query, ["Group Name", "Student Name", "Subject", "Marks"], f"Task 7: Marks for {subject_name} in each group")


def select_8():
    query = (
        session.query(
            Teacher.name,
            Subject.name,
            func.round(func.avg(Mark.mark), 2).label("average_mark"),
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .join(Mark, Mark.subject_id == Subject.id)
        .group_by(Teacher.name, Subject.name)
        .order_by(Teacher.name, Subject.name)
        .all()
    )
    execute_query(query, ["Teacher Name", "Subject", "Average Mark"], "Task 8: Average marks by teachers")


def select_9():
    query = (
        session.query(Student.name, func.array_agg(Subject.name).label("subjects"))
        .join(students_m2m_subjects, Student.id == students_m2m_subjects.c.student_id)
        .join(Subject, Subject.id == students_m2m_subjects.c.subject_id)
        .group_by(Student.name)
        .all()
    )
    execute_query(query, ["Student Name", "Subjects"], "Task 9: Subjects visited by each student")


def select_10():
    query = (
        session.query(
            Student.name, Teacher.name, func.array_agg(Subject.name).label("subjects")
        )
        .join(students_m2m_subjects, Student.id == students_m2m_subjects.c.student_id)
        .join(Subject, Subject.id == students_m2m_subjects.c.subject_id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .group_by(Student.name, Teacher.name)
        .order_by(Student.name, Teacher.name)
        .all()
    )
    execute_query(query, ["Student Name", "Teacher Name", "Subjects"], "Task 10: Subjects taught by teachers to students")

if __name__ == "__main__":
    select_1()
    select_2("History")
    select_3("Computer Science")
    select_4()
    select_5()
    select_6()
    select_7("Mathematics")
    select_8()
    select_9()
    select_10()