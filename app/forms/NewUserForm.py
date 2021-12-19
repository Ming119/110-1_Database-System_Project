from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from wtforms.fields.html5 import EmailField, DateField

class NewUserForm(Form):
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

    submit = SubmitField('Create')

    def validate_password(self, field):
        if not(any(c.isalpha() for c in field.data) and any(c.isdigit() for c in field.data)):
            raise ValidationError('Password must contains number and alphabet')



class NewStaffForm(NewUserForm):
    def __init__(self, *arg, **kwargs):
        self.role = 'staff'
        super(NewStaffForm, self).__init__(*arg, **kwargs)



class NewCustomerForm(NewUserForm):
    def __init__(self, *arg, **kwargs):
        self.role = 'customer'
        super(NewCustomerForm, self).__init__(*arg, **kwargs)

    DOB = DateField('Date of Birth', validators=[
        validators.DataRequired()
    ])
