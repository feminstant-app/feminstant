from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, equal_to, email, ValidationError
from app import Customer


class RegisterForm(FlaskForm):

        def validate_username(self, username_to_check):
            user = Customer.query.filter_by(username=username_to_check.data).first()
            if user:
                raise ValidationError('Username already taken! Please try again')

        def validate_email(self, customer_email_to_check):
            customer_email = Customer.query.filter_by(customer_email=customer_email_to_check.data).first()
            if customer_email:
                raise ValidationError('Email already taken! Please try again')

        customer_name = StringField(label='Name', validators=[DataRequired(), length(min=3, max=100)])
        user_name = StringField(label='Username', validators=[DataRequired(), length(min=3, max=20)])
        customer_email = StringField(label='Email', validators=[DataRequired(), email()])
        password = PasswordField(label='Password', validators=[length(min=6), DataRequired()])
        confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), equal_to('Password')])
        submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField(label='Password', validators=[DataRequired(), length(min=6, max=16)])
    submit = SubmitField(label='Login')
