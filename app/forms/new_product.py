'''
new_product.py
'''

from flask import flash
from flask_wtf import Form
from wtforms import (
    StringField, IntegerField, FloatField, SelectField,
    SubmitField, validators, ValidationError
)



class NewProductForm(Form):
    '''
    Class of New Product Form
    '''

    productName = StringField('Name', validators=[
        validators.DataRequired(),
    ])

    productDescription = StringField('Description')

    image_url = StringField('Image URL', validators=[
        validators.DataRequired(),
    ])

    price = FloatField('Price', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    quantity = IntegerField('Quantity', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    category = SelectField('Category')

    discount = SelectField('Discount Code')

    productSubmit = SubmitField('Submit')

    def __init__(self, categories, discounts, *arg, product=None, **kwargs):
        super().__init__(*arg, **kwargs)
        self.category.choices = [(category.category_id, category.name) for category in categories]
        self.discount.choices = [(None, None)]
        self.discount.choices.extend(
            [(discount.discount_code, discount.discount_code) for discount in discounts]
        )
        if product is not None:
            self.init(product)

    def init(self, product):
        '''
        Initialize the form data with an existing product
        '''

        self.category.default = product.category_id
        self.discount.default = product.discount_code
        self.process()  # pylint: disable=no-member

        self.productName.data        = product.name
        self.productDescription.data = product.description
        self.image_url.data          = product.image_url
        self.price.data              = product.price
        self.quantity.data           = product.quantity

    def validate_price(self, field):    # pylint: disable=no-self-use
        '''
        Validate price
        The input price should not be negative
        '''

        if field.data < 0:
            flash('Price should not be negative.', 'warning')
            raise ValidationError("Price should not be negative.")

    def validate_quantity(self, field): # pylint: disable=no-self-use
        '''
        Validate quantity
        The input quantity should not be negative
        '''

        if field.data < 0:
            flash('Quantity should not be negative.', 'warning')
            raise ValidationError("Quantity should not be negative.")
