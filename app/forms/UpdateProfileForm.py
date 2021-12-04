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

    def __init__(self, user, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.username.data = user.username
        self.first_name.data = user.first_name
        self.last_name.data = user.last_name
