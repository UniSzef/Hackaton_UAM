from app import create_app, db
from app.models import User, Student, Teacher
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Usunięcie wszystkich użytkowników
    db.session.query(Teacher).delete()
    db.session.query(Student).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Tworzenie nauczycieli
    teacher1 = User(username='teacher1', password=generate_password_hash('teacher1pass'), role='teacher')
    teacher2 = User(username='teacher2', password=generate_password_hash('teacher2pass'), role='teacher')

    db.session.add(teacher1)
    db.session.add(teacher2)
    db.session.commit()

    t1 = Teacher(user_id=teacher1.id, first_name='John', last_name='Doe', is_homeroom=True)
    t2 = Teacher(user_id=teacher2.id, first_name='Jane', last_name='Smith', is_homeroom=False)

    db.session.add(t1)
    db.session.add(t2)
    db.session.commit()

    # Tworzenie uczniów
    students = [
        {'username': 'student1', 'password': '1', 'first_name': 'Student1', 'last_name': 'One'},
        {'username': 'student2', 'password': '2', 'first_name': 'Student2', 'last_name': 'Two'},
        {'username': 'student3', 'password': '3', 'first_name': 'Student3', 'last_name': 'Three'},
        {'username': 'student4', 'password': '4', 'first_name': 'Student4', 'last_name': 'Four'},
        {'username': 'student5', 'password': '5', 'first_name': 'Student5', 'last_name': 'Five'},
        {'username': 'student6', 'password': '6', 'first_name': 'Student6', 'last_name': 'Six'},
        {'username': 'student7', 'password': '7', 'first_name': 'Student7', 'last_name': 'Seven'},
        {'username': 'student8', 'password': '8', 'first_name': 'Student8', 'last_name': 'Eight'},
        {'username': 'student9', 'password': '9', 'first_name': 'Student9', 'last_name': 'Nine'},
        {'username': 'student10', 'password': '10', 'first_name': 'Student10', 'last_name': 'Ten'}
    ]

    for student_data in students:
        user = User(username=student_data['username'], password=generate_password_hash(student_data['password']), role='student')
        db.session.add(user)
        db.session.commit()

        student = Student(user_id=user.id, first_name=student_data['first_name'], last_name=student_data['last_name'])
        db.session.add(student)

    db.session.commit()
