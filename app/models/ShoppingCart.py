from app.util import db
from datetime import datetime

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'), primary_key=True)
    cartItmes   = db.relationship('CartItem', backref='shopping_cart')

    amount = db.Column(db.Float(), nullable=False, default=0)



class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_id    = db.Column(db.Integer, db.ForeignKey('shopping_cart.customer_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False, default=0)
    amount   = db.Column(db.Float(), nullable=False, default=0)
