from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators

class UpdateProfileForm(Form):
    username = StringField('Username', validators=[
        validators.DataRequired(),
    ])

    first_name = StringField('First Name', validators=[
        validators.DataRequired(),
    ])

    last_name = StringField('Last Name', validators=[
        validators.DataRequired(),
    ])

    submit = SubmitField('Update')
