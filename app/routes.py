from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Student, Teacher, Grade, Subject, Topic, Post, Attendance
from app.forms import LoginForm, TopicForm, PostForm, AttendanceForm
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/attendance/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def attendance(subject_id):
    form = AttendanceForm()
    students = Student.query.all()
    subject = Subject.query.get(subject_id)

    if request.method == 'POST':
        date = datetime.utcnow().date()

        # Remove existing attendance records for the day
        Attendance.query.filter_by(date=date).delete()
        db.session.commit()

        present_students = []

        # Process the form
        for i, student in enumerate(students):
            is_present = 'students-{}-present'.format(i) in request.form
            attendance = Attendance(date=date, student_id=student.id, present=is_present)
            db.session.add(attendance)
            if is_present:
                present_students.append(student)
        db.session.commit()

        return render_template('attendance_results.html', present_students=present_students)

    while len(form.students) > 0:
        form.students.pop_entry()
    for student in students:
        form.students.append_entry()

    return render_template('attendance.html', form=form, students=students, subject=subject, zip=zip)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
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
    if current_user.role == 'student':
        student = Student.query.filter_by(user_id=current_user.id).first()
        grades = Grade.query.filter_by(student_id=student.id).all()
        grades_by_subject = {}
        for grade in grades:
            subject_name = grade.subject.name
            if subject_name not in grades_by_subject:
                grades_by_subject[subject_name] = []
            grades_by_subject[subject_name].append(grade)
        return render_template('grades.html', grades_by_subject=grades_by_subject)
    return redirect(url_for('main.dashboard'))

@bp.route('/posts/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def posts(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, topic_id=topic_id, user_id=current_user.id, is_anonymous=form.anonymous.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.posts', topic_id=topic_id))
    posts = Post.query.filter_by(topic_id=topic_id).all()
    return render_template('posts.html', topic=topic, posts=posts, form=form)

@bp.route('/topics')
def topics():
    topics = Topic.query.all()
    return render_template('topics.html', topics=topics)

@bp.route('/add_topic', methods=['GET', 'POST'])
@login_required
def add_topic():
    form = TopicForm()
    if form.validate_on_submit():
        new_topic = Topic(title=form.title.data, body=form.body.data, user_id=current_user.id, is_anonymous=form.anonymous.data)
        db.session.add(new_topic)
        db.session.commit()
        return redirect(url_for('main.topics'))
    return render_template('add_topic.html', form=form)

@bp.route('/edit_topic/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def edit_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if current_user.id != topic.user_id:
        flash("You do not have permission to edit this topic.")
        return redirect(url_for('main.topics'))

    form = TopicForm(obj=topic)
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
        flash("You do not have permission to delete this topic.")
        return redirect(url_for('main.topics'))

    db.session.delete(topic)
    db.session.commit()
    flash('Your topic has been deleted.')
    return redirect(url_for('main.topics'))

@bp.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user_id:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('main.posts', topic_id=post.topic_id))

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.content = form.content.data
        post.is_anonymous = form.anonymous.data
        db.session.commit()
        flash('Your post has been updated.')
        return redirect(url_for('main.posts', topic_id=post.topic_id))

    return render_template('edit_post.html', form=form, post=post)

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
                    {'subject_id': 11, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject_id': 12, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Wtorek', 'classes': [
                    {'subject_id': 13, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject_id': 14, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Środa', 'classes': [
                    {'subject_id': 15, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject_id': 16, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Czwartek', 'classes': [
                    {'subject_id': 17, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject_id': 18, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]},
                {'day': 'Piątek', 'classes': [
                    {'subject_id': 19, 'subject': 'Matematyka', 'time': '9:00-9:45', 'room': '102', 'class': '4A'},
                    {'subject_id': 20, 'subject': 'Informatyka', 'time': '10:00-10:45', 'room': '106', 'class': '6B'}
                ]}
            ]
        elif current_user.username == 'teacher2':
            schedule = [
                {'day': 'Poniedziałek', 'classes': [
                    {'subject_id': 21, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject_id': 22, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Wtorek', 'classes': [
                    {'subject_id': 23, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject_id': 24, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Środa', 'classes': [
                    {'subject_id': 25, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject_id': 26, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Czwartek', 'classes': [
                    {'subject_id': 27, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject_id': 28, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]},
                {'day': 'Piątek', 'classes': [
                    {'subject_id': 29, 'subject': 'Biologia', 'time': '8:00-8:45', 'room': '101', 'class': '4A'},
                    {'subject_id': 30, 'subject': 'Chemia', 'time': '11:00-11:45', 'room': '107', 'class': '6B'}
                ]}
            ]
    return render_template('schedule.html', schedule=schedule)