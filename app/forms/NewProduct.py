from flask_wtf import Form;
from wtforms import StringField, FloatField, SelectField, SubmitField, validators;

class NewProduct(Form):
    productName = StringField('Name', validators=[
        validators.DataRequired(),
        validators.Length(1,63)
    ]);

    productDescription = StringField('Description', validators=[
        validators.Length(0,255)
    ]);

    price = FloatField('Price', validators=[
        validators.DataRequired()
    ]);

    category = SelectField('Category');

    discount = StringField('Discount Code');

    productSubmit = SubmitField('Submit');

    def validate_discount(self, field):
        if field.data is not None:
            pass;
