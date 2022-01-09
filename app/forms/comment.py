'''
forms/comment.py
'''

from flask_wtf import Form
from wtforms import IntegerField, TextField, RadioField, SubmitField, validators

class CommentForm(Form):
    '''
    Class of Comment Form
    '''

    product_id = IntegerField('product_id')

    score = RadioField('rating',
        choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        validators = [validators.DataRequired()]
    )

    comment = TextField('comment')

    submit = SubmitField('submit')
