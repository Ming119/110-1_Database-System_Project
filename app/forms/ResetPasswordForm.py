from flask import current_app
from flask_wtf import Form
from wtforms import PasswordField, SubmitField, validators

class ResetPasswordForm(Form):
    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.Length(min=8)
    ])

    password2 = PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='PASSWORD NEED MATCH')   # TODO: message
    ])

    submit = SubmitField('Submit')
