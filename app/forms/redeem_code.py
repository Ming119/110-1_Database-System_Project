'''
redeem_code.py
'''

from flask_wtf import Form
from wtforms import StringField, SubmitField, validators



class RedeemCodeForm(Form):
    '''
    Class of Redeem Code Form
    '''

    code = StringField('Promo Code', validators=[
        validators.DataRequired()
    ])

    submit = SubmitField('Redeem')
