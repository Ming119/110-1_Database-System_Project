from app.util import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'

    order_id    = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'))

    cartItems = db.relationship('OrderItem', backref='order');

    amount = db.Column(db.Integer)

class OrderItem(db.Model):
    __tablename__ = 'cart_item'

    order_id   = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)

    quantity = db.Column(db.Integer)
