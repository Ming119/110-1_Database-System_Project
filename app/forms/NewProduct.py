from util import db
from models.Product import Product
from models.Discount import Discount
from flask import flash
from flask_wtf import Form
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, validators, ValidationError

class NewProduct(Form):
    productName = StringField('Name', validators=[
        validators.DataRequired(),
    ])

    productDescription = StringField('Description')

    price = FloatField('Price', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    quantity = IntegerField('Quantity', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    category = SelectField('Category')

    discount = StringField('Discount Code')

    productSubmit = SubmitField('Submit')

    def validate_productName(self, field):
        if Product.query.filter_by(name=field.data).first() is not None:
            flash(f'Product already exists.', 'warning')
            raise ValidationError("Product already exists.")

    def validate_discount(self, field):
        if field.data != '':
            if Discount.query.filter_by(code=field.data).first() is None:
                flash(f'Discount Code not found.', 'warning')
                raise ValidationError("Discount Code not found.")
