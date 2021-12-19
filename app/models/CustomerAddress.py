from app.util import db
from datetime import datetime

class CustomerAddress(db.Model):
    __tablename__ = 'customer_address'

    address_id = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('customer.user_id'))

    country     = db.Column(db.String(8),   nullable=False)
    city        = db.Column(db.String(32),  nullable=False)
    address     = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(8),   nullable=False)
    telephone   = db.Column(db.String(16),  nullable=False)

    def __repr__(self):
        return '<CustomerAddress {}, {}, {}, {}, {}, {}>'.format(
                    # self.address_id,
                    self.user_id,
                    self.country,
                    self.city,
                    self.address,
                    self.postal_code,
                    self.telephone
                )
