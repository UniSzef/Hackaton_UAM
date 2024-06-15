from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Student, Teacher, Grade, Subject, Topic, Post
from app.forms import LoginForm, TopicForm, PostForm
from werkzeug.security import check_password_hash, generate_password_hash
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('main.grades'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.grades'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.email.data).first()
            if user is None or not check_password_hash(user.password, form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('main.login'))
            login_user(user)
            return redirect(url_for('main.grades'))
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
    schedule = [
        {'day': 'Monday', 'classes': ['Math', 'Science', 'English', 'History', 'PE']},
        {'day': 'Tuesday', 'classes': ['Math', 'Science', 'English', 'Geography', 'Art']},
        {'day': 'Wednesday', 'classes': ['Math', 'Science', 'English', 'History', 'PE']},
        {'day': 'Thursday', 'classes': ['Math', 'Science', 'English', 'Geography', 'Music']},
        {'day': 'Friday', 'classes': ['Math', 'Science', 'English', 'History', 'PE']}
    ]
    return render_template('schedule.html', schedule=schedule)
