from flask_wtf import Form
from wtforms import StringField, FloatField, SubmitField, validators, ValidationError
from wtforms.fields.html5 import DateField, IntegerRangeField

class NewDiscountForm(Form):
    code = StringField('Code', validators=[
        validators.DataRequired("The field {Code} is required.")
    ])

    description = StringField('Description', validators=[
        validators.DataRequired("The field {Description} is required.")
    ])

    start_at = DateField('Start At', validators=[
        validators.DataRequired("The field {Start At} is required.")
    ])

    end_at = DateField('End At', validators=[
        validators.DataRequired("The field {End At} is required.")
    ])

    submit = SubmitField('Submit')

    def initData(self, discount):
        self.code.data        = discount.discount_code
        self.description.data = discount.description
        self.start_at.data    = discount.start_at
        self.end_at.data      = discount.end_at



class NewShippingDiscountForm(NewDiscountForm):
    atLeastAmount = FloatField('Amount Above', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    def __init__(self, *arg, **kwargs):
        self.type = 'shipping'
        super(NewShippingDiscountForm, self).__init__(*arg, **kwargs)

    def initData(self, discount):
        super().initData(discount)
        self.atLeastAmount.data = discount.atLeastAmount



class NewProductDiscountForm(NewDiscountForm):
    discountPercentage = IntegerRangeField('Discount Rate')

    def __init__(self, *arg, **kwargs):
        self.type = 'product'
        super(NewProductDiscountForm, self).__init__(*arg, **kwargs)

    def initData(self, discount):
        super().initData(discount)
        self.discountPercentage.data = discount.discountPercentage



class NewOrderDiscountForm(NewDiscountForm):
    atLeastAmount = FloatField('Amount Above', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    discountPercentage = IntegerRangeField('Discount Rate')

    def __init__(self, *arg, **kwargs):
        self.type = 'ording'
        super(NewOrderDiscountForm, self).__init__(*arg, **kwargs)

    def initData(self, discount):
        super().initData(discount)
        self.atLeastAmount.data      = discount.atLeastAmount
        self.discountPercentage.data = discount.discountPercentage
