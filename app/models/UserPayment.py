from util import db;
from datetime import datetime;

class UserPayment(db.Model):
    __tablename__ = 'user_payment';

    payment_id = db.Column(db.Integer, primary_key=True);

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False);

    payment_type = db.Column(db.String(31),  nullable=False);
    provider     = db.Column(db.String(255), nullable=False);
    account_no   = db.Column(db.Integer,  nullable=False);
    expiry       = db.Column(db.DateTime, nullable=False);

    def __repr__(self):
        return '<UserAddress {}, {}, {}, {}, {}, {}>'.format(
                    self.payment_id,
                    self.user_id,
                    self.payment_type,
                    self.provider,
                    self.account_no,
                    self.expiry,
                );
