from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import SearchField


class Search(Form):
    search = SearchField('Search');
