from datetime import date
from flask_wtf import Form
from wtforms import SubmitField, validators, ValidationError
from wtforms.fields.html5 import DateField



class DateBetweenForm(Form):
    fromDate = DateField('From', validators=[
        validators.DataRequired()
    ])

    toDate = DateField('To', validators=[
        validators.DataRequired()
    ])

    submit = SubmitField('Submit')
