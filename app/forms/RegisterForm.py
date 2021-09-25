from app.db import db;
from models import User;
from flask_wtf import Form;
from wtforms import StringField, SubmitField, validators, PasswordField;
from wtforms.fields.html5 import EmailField;

class RegisterForm(Form):
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 63),
        validators.Email()
    ]);

    username = StringField('UserName', validators=[
        validators.DataRequired(),
        validators.Length(10, 30)
    ]);

    password = PasswordField('PassWord', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ]);

    password2 = PasswordField('Confirm PassWord', validators=[
        validators.DataRequired()
    ]);

    submit = SubmitField('Register New Account');

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register by somebody')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('UserName already register by somebody')
