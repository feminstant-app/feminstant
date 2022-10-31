from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, equal_to, email


class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), length(min=3, max=100)])
    email = StringField(label='Email', validators=[DataRequired(), email()])
    password = PasswordField(label='Password', validators=[DataRequired(), length(min=6)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), equal_to('password')])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), email()])
    password = PasswordField(label='Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField(label='Login')