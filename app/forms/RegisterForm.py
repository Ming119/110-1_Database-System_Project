from util import db;
from models import User;
from flask import flash;
from flask_wtf import Form;
from wtforms import StringField, SubmitField, validators, PasswordField;
from wtforms.fields.html5 import EmailField;

class RegisterForm(Form):
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 63),
        validators.Email()
    ]);

    username = StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(1, 31)
    ]);

    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(8, 31),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ]);

    password2 = PasswordField('Confirm Password', validators=[
        validators.DataRequired()
    ]);

    first_name = StringField('First Name', validators=[
        validators.DataRequired(),
        validators.Length(1, 63)
    ]);

    last_name = StringField('Last Name', validators=[
        validators.DataRequired(),
        validators.Length(1, 63)
    ]);

    submit = SubmitField('Register');

    def validate_email(self, field):
        user = User.User.query.filter_by(email=field.data).first();
        if user:
            if not user.confirm:
                User.User.query.filter_by(email=field.data).delete();
            else:
                flash(f'This email address is already register');
                return redirect(url_for('index.register'));
                # raise ValidationError('Email already register by somebody');

    def validate_username(self, field):
        user = User.User.query.filter_by(username=field.data).first();
        if user:
            if not user.confirm:
                User.User.query.filter_by(email=field.data).delete();
            else:
                flash(f'This username is already register');
                return redirect(url_for('index.register'));
                # raise ValidationError('UserName already register by somebody');
