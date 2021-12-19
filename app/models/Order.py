from app.util import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'

    order_id       = db.Column(db.Integer, primary_key=True)
    customer_id    = db.Column(db.Integer,   db.ForeignKey('customer.user_id'),             nullable=False)
    address_id     = db.Column(db.Integer,   db.ForeignKey('customer_address.address_id'),  nullable=False)
    order_discount = db.Column(db.String(8), db.ForeignKey('order_discount.discount_code'), nullable=True)
    orderItems     = db.relationship('OrderItem', backref='order')

    amount      = db.Column(db.Float(),  nullable=False, default=0)
    shippingFee = db.Column(db.Integer,  nullable=False, default=0)
    shipDate    = db.Column(db.DateTime, nullable=True)
    status      = db.Column(db.Integer,  nullable=False, default=0)

    payment_type = db.Column(db.String(8),  nullable=True)
    provider     = db.Column(db.String(64), nullable=True)
    account_no   = db.Column(db.Integer,    nullable=True)

    create_at = db.Column(db.DateTime, default=datetime.now)



class OrderItem(db.Model):
    __tablename__ = 'order_item'

    order_id   = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False, default=0)
    amount   = db.Column(db.Float(), nullable=False, default=0)
