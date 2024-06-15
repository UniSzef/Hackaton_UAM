from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Student, Teacher, Grade, Subject
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('Nieprawidłowa nazwa użytkownika lub hasło', 'error')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/grades')
@login_required
def grades():
    if current_user.role == 'student':
        student = Student.query.filter_by(user_id=current_user.id).first()
        grades = Grade.query.filter_by(student_id=student.id).all()
        return render_template('grades.html', grades=grades)
    return redirect(url_for('main.dashboard'))

@bp.route('/schedule')
@login_required
def schedule():
    if current_user.role == 'student':
        schedule = [
            {'day': 'Poniedziałek', 'classes': [
                {'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101'},
                {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102'},
                {'subject': 'Angielski', 'time': '10:00-10:45', 'room': '103'},
                {'subject': 'Historia', 'time': '11:00-11:45', 'room': '104'},
                {'subject': 'WF', 'time': '12:00-12:45', 'room': '105'}
            ]},
            {'day': 'Wtorek', 'classes': [
                {'subject': 'Fizyka', 'time': '8:00-8:45', 'room': '101'},
                {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102'},
                {'subject': 'Angielski', 'time': '10:00-10:45', 'room': '103'},
                {'subject': 'Geografia', 'time': '11:00-11:45', 'room': '104'},
                {'subject': 'Plastyka', 'time': '12:00-12:45', 'room': '105'}
            ]},
            {'day': 'Środa', 'classes': [
                {'subject': 'Chemia', 'time': '8:00-8:45', 'room': '101'},
                {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102'},
                {'subject': 'Angielski', 'time': '10:00-10:45', 'room': '103'},
                {'subject': 'Historia', 'time': '11:00-11:45', 'room': '104'},
                {'subject': 'WF', 'time': '12:00-12:45', 'room': '105'}
            ]},
            {'day': 'Czwartek', 'classes': [
                {'subject': 'Geografia', 'time': '8:00-8:45', 'room': '101'},
                {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102'},
                {'subject': 'Angielski', 'time': '10:00-10:45', 'room': '103'},
                {'subject': 'Biologia', 'time': '11:00-11:45', 'room': '104'},
                {'subject': 'Muzyka', 'time': '12:00-12:45', 'room': '105'}
            ]},
            {'day': 'Piątek', 'classes': [
                {'subject': 'Historia', 'time': '8:00-8:45', 'room': '101'},
                {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102'},
                {'subject': 'Angielski', 'time': '10:00-10:45', 'room': '103'},
                {'subject': 'Chemia', 'time': '11:00-11:45', 'room': '104'},
                {'subject': 'WF', 'time': '12:00-12:45', 'room': '105'}
            ]}
        ]
    elif current_user.role == 'teacher':
        if current_user.username == 'teacher1':
            schedule = [
                {'day': 'Poniedziałek', 'classes': [
                    {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Wtorek', 'classes': [
                    {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Środa', 'classes': [
                    {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Czwartek', 'classes': [
                    {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Piątek', 'classes': [
                    {'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]}
            ]
        elif current_user.username == 'teacher2':
            schedule = [
                {'day': 'Poniedziałek', 'classes': [
                    {'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Wtorek', 'classes': [
                    {'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Środa', 'classes': [
                    {'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Czwartek', 'classes': [
                    {'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Piątek', 'classes': [
                    {'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]}
            ]
    return render_template('schedule.html', schedule=schedule)
