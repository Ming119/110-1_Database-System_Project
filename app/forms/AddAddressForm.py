from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, SubmitField, validators
from country_list import countries_for_language

class AddAddressForm(Form):
    country = SelectField('Country', validators=[
        validators.DataRequired(),
    ])

    city = StringField('City', validators=[
        validators.DataRequired(),
    ])

    address = StringField('Address', validators=[
        validators.DataRequired(),
    ])

    postal_code = StringField('Postal Code', validators=[
        validators.DataRequired(),
    ])

    telephone = IntegerField('Telephone', validators=[
        validators.DataRequired(),
    ])

    submit = StringField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddAddressForm, self).__init__(*args, **kwargs)

        self.country.choices = countries_for_language('en')
        self.country.default = 'TW'
        self.process()


    # def validate_postal_code(self, field):
