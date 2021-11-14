from app.util import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'order'

    order_id    = db.Column(db.Integer, primary_key=True)
    customer_id = db.column(db.Integer, db.ForeignKey('customer.user_id'))
    cart_id     = db.column(db.Integer, db.ForeignKey('shopping_cart.cart_id'))
    address_id  = db.column(db.Integer, db.ForeignKey('customer_address.address_id'))
    payment_id  = db.column(db.Integer, db.ForeignKey('customer_payment.payment_id'))
