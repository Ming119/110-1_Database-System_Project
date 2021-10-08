from util import db;
from models.ProductCategory import ProductCategory;
from flask import flash, redirect, url_for;
from flask_wtf import Form;
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError;

class NewCategory(Form):
    categoryName = StringField('Category Name', validators=[
        validators.DataRequired(),
        validators.Length(1, 63)
    ]);

    categoryDescription = TextAreaField('Category Description', validators=[
        validators.Length(0, 255)
    ]);

    categorySubmit = SubmitField('Submit');

    def validate_categoryName(self, field):
        if ProductCategory.query.filter_by(name=field.data).first() is not None:
            flash(f'Category already exists.', 'warning');
            raise ValidationError("Category already exists.")
