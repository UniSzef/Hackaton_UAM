from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=1, max=128)])
    submit = SubmitField('Zaloguj się')

class TopicForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    body = TextAreaField('Treść', validators=[DataRequired()])
    anonymous = BooleanField('Utwórz jako anonimowy')  # Anonymity checkbox
    submit = SubmitField('Wyślij')

class PostForm(FlaskForm):
    content = TextAreaField('Treść', validators=[DataRequired()])
    anonymous = BooleanField('Utwórz jako anonimowy')  # Anonymity checkbox
    submit = SubmitField('Dodaj Post')
