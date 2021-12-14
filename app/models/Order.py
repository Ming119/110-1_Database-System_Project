from app.util import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'

    order_id    = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'))
    address_id  = db.Column(db.Integer, db.ForeignKey('customer_address.address_id'))
    order_discount    = db.Column(db.String(8), db.ForeignKey('order_discount.discount_code'))

    cartItems = db.relationship('OrderItem', backref='order');

    amount      = db.Column(db.Integer)
    shippingFee = db.Column(db.Integer)
    shipDate    = db.Column(db.DateTime)
    status      = db.Column(db.Integer)

    create_at = db.Column(db.DateTime, default=datetime.now)



class OrderItem(db.Model):
    __tablename__ = 'cart_item'

    order_id   = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)

    quantity = db.Column(db.Integer)
    amount   = db.Column(db.Integer)
