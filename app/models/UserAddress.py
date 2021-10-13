from util import db
from datetime import datetime


class UserAddress(db.Model):
    __tablename__ = 'user_address'

    address_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    country     = db.Column(db.String(255), nullable=False)
    city        = db.Column(db.String(255), nullable=False)
    address     = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(7),   nullable=False)
    telephone   = db.Column(db.String(15),  nullable=False)

    def __repr__(self):
        return '<UserAddress %r>' % (
            self.address_id,
            self.user_id,
            self.country,
            self.city,
            self.address,
            self.postal_code,
            self.telephone
        )
