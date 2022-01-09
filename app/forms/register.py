'''
register.py
'''

from datetime import date
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from wtforms.fields.html5 import EmailField, DateField



class RegisterForm(Form):
    '''
    Class of Register Form
    '''

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Email()
    ])

    username = StringField('Username', validators=[
        validators.DataRequired(),
    ])

    first_name = StringField('First Name', validators=[
        validators.DataRequired(),
    ])

    last_name = StringField('Last Name', validators=[
        validators.DataRequired(),
    ])

    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(min=8)
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords do not match.')
    ])

    dob = DateField('Date of Birth', validators=[
        validators.DataRequired()
    ])

    submit = SubmitField('Register')

    def validate_password(self, field): # pylint: disable=no-self-use
        '''
        Validate password
        The input password should contains number and alphabet
        '''

        if not(any(c.isalpha() for c in field.data) and any(c.isdigit() for c in field.data)):
            raise ValidationError('Password must contains number and alphabet.')

    def validate_dob(self, field):      # pylint: disable=no-self-use
        '''
        Validate date of birth
        The input date of birth should before the current day
        '''

        if field.data > date.today():
            raise ValidationError('Date must before today.')
