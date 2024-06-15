<<<<<<< HEAD
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app import db, create_app
from app.models import User
from app.forms import LoginForm

app = create_app()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the e-dziennik!"
=======
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
            flash('Invalid username or password')
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
    schedule = [
        {'day': 'Monday', 'classes': ['Math', 'Science', 'English', 'History', 'PE']},
        {'day': 'Tuesday', 'classes': ['Math', 'Science', 'English', 'Geography', 'Art']},
        {'day': 'Wednesday', 'classes': ['Math', 'Science', 'English', 'History', 'PE']},
        {'day': 'Thursday', 'classes': ['Math', 'Science', 'English', 'Geography', 'Music']},
        {'day': 'Friday', 'classes': ['Math', 'Science', 'English', 'History', 'PE']}
    ]
    return render_template('schedule.html', schedule=schedule)
>>>>>>> main
