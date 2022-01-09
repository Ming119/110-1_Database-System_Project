'''
reset_password.py
'''

from flask_wtf import Form
from wtforms import PasswordField, SubmitField, validators



class ResetPasswordForm(Form):
    '''
    Class of Reset Password Form
    '''

    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.Length(min=8)
    ])

    password2 = PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='PASSWORD NEEDS TO MATCH')
    ])

    submit = SubmitField('Submit')
