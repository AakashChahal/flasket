from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already Exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use!')

    username = StringField(label='Username: ', validators=[Length(min=4), DataRequired()])
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Log In')


class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase')


class SellForm(FlaskForm):
    submit = SubmitField(label='Sell')