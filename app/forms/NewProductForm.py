from app.models.Discount import Discount
from flask import flash
from flask_wtf import Form
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField, validators, ValidationError

class NewProductForm(Form):
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

    discount = StringField('Discount Code')

    productSubmit = SubmitField('Submit')

    def __init__(self, categories, product=None, *arg, **kwargs):
        super(NewProductForm, self).__init__(*arg, **kwargs)
        self.category.choices = [(category.category_id, category.name) for category in categories if (category.is_active)]
        if product is not None:
            self.initProductData(product)

    def initProductData(self, product):
        self.productName.data        = product.name
        self.productDescription.data = product.description
        self.image_url.data          = product.image_url
        self.price.data              = product.price
        self.quantity.data           = product.quantity
        self.category.default        = product.category_id

    def validate_price(self, field):
        if field.data < 0:
            flash(f'Price should not be negative.', 'warning')
            raise ValidationError("Price should not be negative.")

    def validate_quantity(self, field):
        if field.data < 0:
            flash(f'Quantity should not be negative.', 'warning')
            raise ValidationError("Quantity should not be negative.")

    def validate_discount(self, field):
        if field.data != '' and Discount.query.filter_by(code=field.data).first() is None:
            flash(f'Discount Code not found.', 'warning')
            raise ValidationError("Discount Code not found.")
