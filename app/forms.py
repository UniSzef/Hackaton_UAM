from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, Length
from wtforms.fields import FieldList, FormField

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


class StudentAttendanceForm(FlaskForm):
    present = BooleanField('Obecny')

class AttendanceForm(FlaskForm):
    students = FieldList(FormField(StudentAttendanceForm))
    submit = SubmitField('Zapisz Obecność')
