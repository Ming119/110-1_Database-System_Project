from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import SearchField

class SearchForm(Form):
    search = SearchField('Search')