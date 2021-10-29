from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField, DateField

class RegisterForm(Form):
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
        validators.EqualTo('password', message='PASSWORD NEEDS TO MATCH')
    ])

    DOB = DateField('Date of Birth', validators=[
        validators.DataRequired()
    ])

    submit = SubmitField('Register')

    # TODO: error message
    def validate_password(self, field):
        if not(any(not c.isalnum() for c in field.data) and any(c.isupper() for c in field.data) and any(c.islower() for c in field.data) and any(c.isdigit() for c in field.data)):
            raise ValidationError('Password must contains number, upper case, lower case and special character.')
