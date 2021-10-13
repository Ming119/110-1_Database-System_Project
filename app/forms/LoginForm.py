from flask import current_app
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators

class LoginForm(Form):
    username = StringField('Username', validators=[
        validators.DataRequired(),
    ])

    password = PasswordField('Password', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('Remember me')

    submit = SubmitField('Login')
