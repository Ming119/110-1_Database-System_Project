'''
add_to_cart.py
'''

from flask_wtf import Form
from wtforms import IntegerField, SubmitField, validators



class AddToCartForm(Form):
    '''
    Class of Add To Cart Form
    '''

    quantity = IntegerField('Quantity', validators=[
        validators.NumberRange(min=1)
    ])

    addToCard = SubmitField('Add To Card')
