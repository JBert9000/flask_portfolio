from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from portfolio.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username',
        validators=[DataRequired(), Length(min=2,max=20)])
    email=StringField('Email',
        validators=[DataRequired(),Email()])
    password=PasswordField('Password',
        validators=[DataRequired(),Length(min=6,max=20)])
    confirm_password=PasswordField('Confirm Password',
        validators=[DataRequired(),Length(min=6,max=20),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use. Please select another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please select another one.')


class LoginForm(FlaskForm):
    email=StringField('Email',
        validators=[DataRequired()])
    password=PasswordField('Password',
        validators=[DataRequired()])
    rememeber=BooleanField('Rememeber Me')
    submit=SubmitField('Login')
