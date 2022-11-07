from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
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
    house = StringField(label='House Name or Number')
    street = StringField(label='Street')
    city = StringField(label='Town or City')
    postcode = StringField(label='Post Code', validators=[DataRequired(), length(min=6, max=8)])
    submit = SubmitField(label='Go to Payment')

    def validate_house(form, field):
        if len(field.data) < 1:
            raise ValidationError("That isn't a valid house name or number")

    def validate_street(form, field):
        if len(field.data) < 1:
            raise ValidationError("That isn't a valid street")

    def validate_city(form, field):
        if len(field.data) < 1:
            raise ValidationError("That isn't a valid city")
