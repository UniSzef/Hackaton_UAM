from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Student, Teacher, Grade, Subject, Topic, Post, Attendance
from app.forms import LoginForm, TopicForm, PostForm
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from app.forms import AttendanceForm
from datetime import datetime
import random



bp = Blueprint('main', __name__)

@bp.route('/attendance/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
def attendance(lesson_id):
    form = AttendanceForm()
    students = Student.query.all()
    
    if request.method == 'POST':
        date = datetime.utcnow().date()
        
        # Usuń istniejące rekordy obecności dla danego dnia
        Attendance.query.filter_by(date=date).delete()
        db.session.commit()
        
        # Przetwarzanie formularza
        for i, student in enumerate(students):
            is_present = 'students-{}-present'.format(i) in request.form
            attendance = Attendance(date=date, student_id=student.id, present=is_present)
            db.session.add(attendance)
        db.session.commit()
        
        flash('Attendance recorded successfully.')
        return redirect(url_for('main.schedule'))
    
    # Pre-populate form with students
    while len(form.students) > 0:
        form.students.pop_entry()
    for student in students:
        form.students.append_entry()
    
    return render_template('attendance.html', form=form, students=students, zip=zip)





@bp.route('/wheel_of_fortune', methods=['GET', 'POST'])
@login_required
def wheel_of_fortune():
    date = datetime.utcnow().date()
    present_students = Student.query.join(Attendance).filter(Attendance.date == date, Attendance.present == True).all()
    selected_student = None
    if request.method == 'POST':
        if present_students:
            selected_student = random.choice(present_students)
            print(f'The chosen student is: {selected_student.first_name} {selected_student.last_name}')
        else:
            print('No students are present today.')
    return render_template('wheel_of_fortune.html', students=present_students, selected_student=selected_student)



@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.email.data).first()
            if user is None or not check_password_hash(user.password, form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('main.login'))
            login_user(user)
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            logging.error(f"Error during login: {e}")
            flash('An error occurred during login')
            return redirect(url_for('main.login'))
    return render_template('login.html', form=form)

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
    try:
        if current_user.role == 'student':
            student = Student.query.filter_by(user_id=current_user.id).first()
            grades = Grade.query.filter_by(student_id=student.id).all()
            return render_template('grades.html', grades=grades)
        else:
            return redirect(url_for('main.dashboard'))
    except Exception as e:
        logging.error(f"Error fetching grades: {e}")
        flash('An error occurred while fetching grades')
        return redirect(url_for('main.dashboard'))

@bp.route('/topics')
def topics():
    try:
        topics = Topic.query.all()
        return render_template('topics.html', topics=topics)
    except Exception as e:
        logging.error(f"Error fetching topics: {e}")
        flash('An error occurred while fetching topics')
        return redirect(url_for('main.grades'))

@bp.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def posts(topic_id):
    try:
        topic = Topic.query.get_or_404(topic_id)
        posts = Post.query.filter_by(topic_id=topic_id).all()
        form = PostForm()
        if form.validate_on_submit():
            new_post = Post(content=form.content.data, topic_id=topic_id, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('main.posts', topic_id=topic_id))
        return render_template('posts.html', topic=topic, posts=posts, form=form)
    except Exception as e:
        logging.error(f"Error fetching posts or creating a new post: {e}")
        flash('An error occurred while fetching posts or creating a new post')
        return redirect(url_for('main.topics'))

@bp.route('/add_topic', methods=['GET', 'POST'])
@login_required
def add_topic():
    form = TopicForm()
    if form.validate_on_submit():
        try:
            new_topic = Topic(title=form.title.data, body=form.body.data, user_id=current_user.id)
            db.session.add(new_topic)
            db.session.commit()
            return redirect(url_for('main.topics'))
        except Exception as e:
            logging.error(f"Error adding new topic: {e}")
            flash('An error occurred while adding the topic')
            return redirect(url_for('main.add_topic'))
    return render_template('add_topic.html', form=form)

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
                    {'id': 11, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'id': 12, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Wtorek', 'classes': [
                    {'id': 13, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'id': 14, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Środa', 'classes': [
                    {'id': 15, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'id': 16, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Czwartek', 'classes': [
                    {'id': 17, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'id': 18, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Piątek', 'classes': [
                    {'id': 19, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'id': 20, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]}
            ]
        elif current_user.username == 'teacher2':
            schedule = [
                {'day': 'Poniedziałek', 'classes': [
                    {'id': 21, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'id': 22, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Wtorek', 'classes': [
                    {'id': 23, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'id': 24, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Środa', 'classes': [
                    {'id': 25, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'id': 26, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Czwartek', 'classes': [
                    {'id': 27, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'id': 28, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Piątek', 'classes': [
                    {'id': 29, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'id': 30, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]}
            ]
    return render_template('schedule.html', schedule=schedule)

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('main.posts', topic_id=post.topic_id))

    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.')
        return redirect(url_for('main.posts', topic_id=post.topic_id))
    elif request.method == 'GET':
        form.content.data = post.content

    return render_template('edit_post.html', form=form)

@bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        flash('You do not have permission to delete this post.')
        return redirect(url_for('main.posts', topic_id=post.topic_id))

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('main.posts', topic_id=post.topic_id))

@bp.route('/edit_topic/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def edit_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if current_user.id != topic.user_id:
        flash('You do not have permission to edit this topic.')
        return redirect(url_for('main.topics'))

    form = TopicForm(obj=topic)  # Pre-fill form
    if form.validate_on_submit():
        topic.title = form.title.data
        topic.body = form.body.data
        db.session.commit()
        flash('Your topic has been updated.')
        return redirect(url_for('main.topics'))
    return render_template('edit_topic.html', form=form)

@bp.route('/delete_topic/<int:topic_id>', methods=['POST'])
@login_required
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if current_user.id != topic.user_id:
        flash('You do not have permission to delete this topic.')
        return redirect(url_for('main.topics'))

    db.session.delete(topic)
    db.session.commit()
    flash('Your topic has been deleted.')
    return redirect(url_for('main.topics'))