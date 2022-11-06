from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
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


class CheckoutForm(FlaskForm):
    inputAddress1 = StringField(label='Address Line 1', validators=[DataRequired()])
    inputAddress2 = StringField(label='Address Line 2', validators=[DataRequired()])
    inputCity = StringField(label='City', validators=[DataRequired()])
    inputZip = StringField(label='Post Code', validators=[DataRequired()])
    submit = SubmitField(label='Checkout')


class BasketForm(FlaskForm):
    submit = SubmitField(label='Add to basket', validators=[DataRequired()])


class PaymentForm(FlaskForm):
    submit = SubmitField(label='Confirm Pay')
