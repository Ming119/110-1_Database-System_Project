'''
search.py
'''

from flask_wtf import Form
from wtforms.fields.html5 import SearchField



class SearchForm(Form):
    '''
    Class of Search Form
    '''

    search = SearchField('Search')
