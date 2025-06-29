from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(), Length(min=3, max=100)])
    password = PasswordField('Password', validators=[
        InputRequired(), Length(min=3, max=100)])
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    name = StringField('Student Name', validators=[
        InputRequired(), Length(min=2, max=150)])
    roll_no = StringField('Roll Number', validators=[
        InputRequired(), Length(min=1, max=50)])

    subject1 = IntegerField('Subject 1 Marks', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    subject2 = IntegerField('Subject 2 Marks', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    subject3 = IntegerField('Subject 3 Marks', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    subject4 = IntegerField('Subject 4 Marks', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    subject5 = IntegerField('Subject 5 Marks', validators=[
        InputRequired(), NumberRange(min=0, max=100)])

    submit = SubmitField('Submit')
