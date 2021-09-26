from util import db;
from models import User;
from flask import flash;
from flask_wtf import Form;
from wtforms import StringField, SubmitField, validators, PasswordField, BooleanField;
from wtforms.fields.html5 import EmailField;

class LoginForm(Form):
    username = StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(1, 31)
    ]);

    password = PasswordField('Password', validators=[
        validators.DataRequired()
    ]);

    remember_me = BooleanField('Remember me')

    submit = SubmitField('Login');
