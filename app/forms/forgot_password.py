'''
forgot_password.py
'''

from flask_wtf import Form
from wtforms import SubmitField, validators
from wtforms.fields.html5 import EmailField



class ForgotPasswordForm(Form):
    '''
    Class of Forgot Password Form
    '''

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Email()
    ])

    submit = SubmitField('Reset your Password')
