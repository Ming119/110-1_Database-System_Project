from app.util import db
from datetime import datetime

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'

    cart_id     = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'))

    cartItem = db.relationship('CartItem', backref='shopping_cart')

    amount = db.Column(db.Integer)

class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_id    = db.Column(db.Integer, db.ForeignKey('shopping_cart.cart_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)
    # prodcut = db.relationship('Product', primaryjoin='foreign(CartItem.product_id)==Product.product_id')
    # discount_id

    quantity = db.Column(db.Integer)
