from app.db import db;
from models import User;
from flask_wtf import Form;
from wtforms import StringField, SubmitField, validators, PasswordField;
from wtforms.fields.html5 import EmailField;

class LoginForm(Form):
    username = StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(1, 31)
    ]);

    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(8, 31)
    ]);

    submit = SubmitField('Login');
