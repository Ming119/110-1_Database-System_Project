from app.util import db
from datetime import datetime

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'), primary_key=True)

    product_id  = db.relationship('Product', backref='shopping_cart')
