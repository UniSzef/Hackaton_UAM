from flask import render_template
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return "Welcome to the e-dziennik!"