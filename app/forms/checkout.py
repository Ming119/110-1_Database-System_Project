'''
checkout.py
'''

from flask_wtf import Form
from wtforms import IntegerField, StringField, RadioField, SubmitField, validators



class CheckoutForm(Form):
    '''
    Class of Checkout Form
    '''

    addresses = RadioField('Address')

    paymentType = RadioField('Payment',
        choices = [('Cash', 'Cash on delivery'), ('Credit', 'Credit card')]
    )

    CreditCardNumber = IntegerField('Credit Card Number', validators=[validators.Optional()])

    Expiration = StringField('Expiration')

    CVV = IntegerField('CVV', validators=[validators.Optional()])

    submit = SubmitField('Checkout')

    def __init__(self, addresses, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.addresses.choices = list(
            (address.address_id, address.address) for address in addresses
        )

    def init(self):
        '''
        Initialize the form data
        '''

        self.paymentType.default = "Cash"
        self.addresses.default = self.addresses.choices[0][0]
        self.process()  #pylint: disable=no-member
