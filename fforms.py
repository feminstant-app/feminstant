# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
#
#
# class RegisterForm(FlaskForm):
#     username = StringField(label='User Name:')
#     email = StringField(label='Email Address:')
#     password1 = PasswordField(label='Password:')
#     password2 = PasswordField(label='Confirm Password:')
#     submit = SubmitField(label='Create Account')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import data_required, length, equal_to, email


class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[data_required(), length(min=3, max=20)])
    email = StringField(label='Email', validators=[data_required(), email()])
    password = PasswordField(label='Password', validators=[data_required(), length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[data_required(), equal_to('Password')])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[data_required(), length(min=3, max=20)])
    password = PasswordField(label='Password', validators=[data_required(), length(min=6, max=16)])
    submit = SubmitField(label='Login')