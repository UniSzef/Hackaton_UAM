from app import create_app, db
from app.models import User, Student, Teacher, Subject, Grade
from werkzeug.security import generate_password_hash
import random
app = create_app()

with app.app_context():
    # Usunięcie wszystkich użytkowników
    db.session.query(Grade).delete()
    db.session.query(Subject).delete()
    db.session.query(Teacher).delete()
    db.session.query(Student).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Tworzenie nauczycieli
    teacher1 = User(username='teacher1', password=generate_password_hash('1'), role='teacher')
    teacher2 = User(username='teacher2', password=generate_password_hash('2'), role='teacher')

    db.session.add(teacher1)
    db.session.add(teacher2)
    db.session.commit()

    t1 = Teacher(user_id=teacher1.id, first_name='Jan', last_name='Kowalski', is_homeroom=True)
    t2 = Teacher(user_id=teacher2.id, first_name='Anna', last_name='Nowak', is_homeroom=False)

    db.session.add(t1)
    db.session.add(t2)
    db.session.commit()

    # Tworzenie przedmiotów
    math = Subject(name='Matematyka', teacher_id=t1.id)
    biology = Subject(name='Biologia', teacher_id=t2.id)
    english = Subject(name='Angielski', teacher_id=t1.id)
    history = Subject(name='Historia', teacher_id=t2.id)

    db.session.add(math)
    db.session.add(biology)
    db.session.add(english)
    db.session.add(history)
    db.session.commit()

    # Tworzenie uczniów
    students = [
        {'username': 'student1', 'password': '1', 'first_name': 'Wiktoria', 'last_name': 'Bąk'},
        {'username': 'student2', 'password': '2', 'first_name': 'Anna', 'last_name': 'Lewandowska'},
        {'username': 'student3', 'password': '3', 'first_name': 'Piotr', 'last_name': 'Wiśniewski'},
        {'username': 'student4', 'password': '4', 'first_name': 'Maria', 'last_name': 'Wójcik'},
        {'username': 'student5', 'password': '5', 'first_name': 'Adam', 'last_name': 'Andrzejewski'},
        {'username': 'student6', 'password': '6', 'first_name': 'Marta', 'last_name': 'Broda'},
        {'username': 'student7', 'password': '7', 'first_name': 'Robert', 'last_name': 'Liszkiewicz'},
        {'username': 'student8', 'password': '8', 'first_name': 'Paweł', 'last_name': 'Zieliński'},
        {'username': 'student9', 'password': '9', 'first_name': 'Ewa', 'last_name': 'Szymańska'},
        {'username': 'student10', 'password': '10', 'first_name': 'Tomasz', 'last_name': 'Woźniak'}
    ]

    subjects = [math, biology, english, history]

    for student_data in students:
        user = User(username=student_data['username'], password=generate_password_hash(student_data['password']), role='student')
        db.session.add(user)
        db.session.commit()

        student = Student(user_id=user.id, first_name=student_data['first_name'], last_name=student_data['last_name'])
        db.session.add(student)
        db.session.commit()

        # Dodawanie ocen dla ucznia
        grades = []
        for subject in subjects:
            # Generate between 2 to 5 grades for each subject
            for _ in range(random.randint(2, 5)):
                grade = Grade(student_id=student.id, subject_id=subject.id, grade=str(random.randint(1, 6)))
                grades.append(grade)
        
        db.session.add_all(grades)

    db.session.commit()
