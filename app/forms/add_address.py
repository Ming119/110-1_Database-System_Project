from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, validators
from country_list import countries_for_language

'''
'''

class AddAddressForm(Form):
    '''
    '''

    country = SelectField('Country')

    city = StringField('City', validators=[
        validators.DataRequired(),
    ])

    address = StringField('Address', validators=[
        validators.DataRequired(),
    ])

    postal_code = StringField('Postal Code', validators=[
        validators.DataRequired(),
    ])

    telephone = StringField('Telephone', validators=[
        validators.DataRequired()
    ])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country.choices = countries_for_language('en')
        self.country.default = 'TW'
