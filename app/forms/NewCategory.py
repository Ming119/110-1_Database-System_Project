from flask_wtf import Form
from wtforms import StringField, SubmitField, validators


class NewCategory(Form):
    name = StringField('Name', validators=[
        validators.DataRequired(),
    ])

    description = StringField('Description')

    submit = SubmitField('Submit')
