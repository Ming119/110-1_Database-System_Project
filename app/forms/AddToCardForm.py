from flask_wtf import Form
from wtforms import IntegerField, SubmitField, validators

class AddToCardForm(Form):
    quantity = IntegerField('Quantity', validators=[])

    addToCard = SubmitField('addToCard')
