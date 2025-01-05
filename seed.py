from connect import session
import random
from models import Student, Group, Subject, Teacher, Mark
from faker import Faker

fake = Faker()

def create_groups():
    return [Group(name=f"Group {i+1}") for i in range(3)]

def create_teachers():
    return [Teacher(name=fake.name()) for _ in range(8)]

def create_subjects(teachers):
    courses = [
        "Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography",
        "English", "French", "German", "Spanish", "Music", "Art", "Computer Science"
    ]
    return [Subject(name=course, teacher=random.choice(teachers)) for course in courses]

def create_students(groups, subjects):
    students = [
        Student(
            name=fake.name(),
            age=random.randint(10, 20),
            groups=random.sample(groups, k=random.randint(1, 2)),
            subjects=random.sample(subjects, k=random.randint(8, 10))
        )
        for _ in range(39)
    ]
    return students

def create_marks(students):
    marks = [
        Mark(
            mark=random.randint(1, 12),
            student=student,
            subject=random.choice(student.subjects),
            obtained_at=fake.date_time_between(start_date="-1y", end_date="now")
        )
        for student in students
        for _ in range(random.randint(12, 20))
    ]
    return marks

def main():
    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    students = create_students(groups, subjects)
    marks = create_marks(students)

    session.add_all(groups)
    session.add_all(teachers)
    session.add_all(subjects)
    session.add_all(students)
    session.add_all(marks)
    session.commit()
    session.close()

if __name__ == "__main__":
    main()