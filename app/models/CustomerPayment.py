from app.util import db
from datetime import datetime

class CustomerPayment(db.Model):
    __tablename__ = 'customer_payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('customer.user_id'), nullable=False)

    payment_type = db.Column(db.String(8),  nullable=False)
    provider     = db.Column(db.String(64), nullable=False)
    account_no   = db.Column(db.Integer,  nullable=False)
    expiry       = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<UserAddress {}, {}, {}, {}, {}, {}>'.format(
                    self.payment_id,
                    self.user_id,
                    self.payment_type,
                    self.provider,
                    self.account_no,
                    self.expiry,
                )
