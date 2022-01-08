from flask_wtf import Form
from wtforms import StringField, FloatField, SubmitField, validators
from wtforms.fields.html5 import DateField, IntegerRangeField

'''
'''

class NewDiscountForm(Form):
    '''
    Base class for creating new discount
    '''

    code = StringField('Code')

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

    def init(self, discount):
        '''
        Initialize the form data with an existing discount
        '''

        self.code.data        = discount.discount_code
        self.description.data = discount.description
        self.start_at.data    = discount.start_at
        self.end_at.data      = discount.end_at



class NewShippingDiscountForm(NewDiscountForm):
    '''
    Inherited from NewDiscountForm
    For creating a new shipping discount
    '''

    atLeastAmount = FloatField('Amount Above', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    def __init__(self, *arg, **kwargs):
        self.type = 'shipping'
        super().__init__(*arg, **kwargs)

    def init(self, discount):
        '''
        Initialize the shipping form data with an existing discount
        '''

        super().init(discount)
        self.atLeastAmount.data = discount.atLeastAmount



class NewProductDiscountForm(NewDiscountForm):
    '''
    Inherited from NewDiscountForm
    For creating a new product discount
    '''

    discountPercentage = IntegerRangeField('Discount Rate')

    def __init__(self, *arg, **kwargs):
        self.type = 'product'
        super().__init__(*arg, **kwargs)

    def init(self, discount):
        '''
        Initialize the product form data with an existing discount
        '''

        super().init(discount)
        self.discountPercentage.data = discount.discountPercentage



class NewOrderDiscountForm(NewDiscountForm):
    '''
    Inherited from NewDiscountForm
    For creating a new order discount
    '''

    atLeastAmount = FloatField('Amount Above', validators=[
        validators.InputRequired(),
        validators.NumberRange(min=0)
    ])

    discountPercentage = IntegerRangeField('Discount Rate')

    def __init__(self, *arg, **kwargs):
        self.type = 'ording'
        super().__init__(*arg, **kwargs)

    def init(self, discount):
        '''
        Initialize the order form data with an existing discount
        '''

        super().init(discount)
        self.atLeastAmount.data      = discount.atLeastAmount
        self.discountPercentage.data = discount.discountPercentage
