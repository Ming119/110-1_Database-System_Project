from flask_wtf import Form
from wtforms import IntegerField, StringField, RadioField, SubmitField, validators

class CheckoutForm(Form):
    addresses = RadioField('Address')

    paymentType = RadioField('Payment',
        choices=[('Cash', 'Cash on delivery'), ('Credit', 'Credit card')],
    )

    CreditCardNumber = IntegerField('Credit Card Number', validators=[validators.Optional()])

    Expiration = StringField('Expiration')

    CVV = IntegerField('CVV', validators=[validators.Optional()])

    submit = SubmitField('Checkout')

    def __init__(self, addresses, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)

        self.addresses.choices = list((address.address_id, address.address) for address in addresses)

    def init(self):
        self.paymentType.default = "Cash"
        if self.addresses.choices:
            self.addresses.default = self.addresses.choices[0][0]
        self.process()
