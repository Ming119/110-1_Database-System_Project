from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators

class NewCategoryForm(Form):
    categoryName = StringField('Category Name', validators=[
        validators.DataRequired(),
    ])

    categoryDescription = TextAreaField('Category Description')

    categorySubmit = SubmitField('Submit')
