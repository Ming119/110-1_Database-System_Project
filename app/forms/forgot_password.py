from flask_wtf import Form
from wtforms import SubmitField, validators
from wtforms.fields.html5 import EmailField

'''
'''

class ForgotPasswordForm(Form):
    '''
    '''
    
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Email()
    ])

    submit = SubmitField('Reset your Password')
