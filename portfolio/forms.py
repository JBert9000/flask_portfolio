from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username=StringField('Username',
        validators=[DataRequired(), Length(min=2,max=20)])
    email=StringField('Email',
        validators=[DataRequired(),Email()])
    password=PasswordField('Password',
        validators=[DataRequired(),Length(min=6,max=20)])
    confirm_passowrd=PasswordField('Confirm Password',
        validators=[DataRequired(),Length(min=6,max=20),EqualTo('password')])
    submit=SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email=StringField('Email',
        validators=[DataRequired()])
    passowrd=PasswordField('Password',
        validators=[DataRequired()])
    rememeber=BooleanField('Rememeber Me')
    submit=SubmitField('Login')
