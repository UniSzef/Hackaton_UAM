from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=128)])
    submit = SubmitField('Log In')

class TopicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    anonymous = BooleanField('Create as Anonymous')  # Anonymity checkbox
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    anonymous = BooleanField('Create as Anonymous')  # Anonymity checkbox
    submit = SubmitField('Add Post')