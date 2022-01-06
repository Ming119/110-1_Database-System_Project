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

    @staticmethod
    def create(user_id, country, city, address, postal_code, telephone):
        try:
            db.session.add(CustomerAddress(
                user_id     = user_id,
                country     = country,
                city        = city,
                address     = address,
                postal_code = postal_code,
                telephone   = telephone
            ))
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def getAllByID(user_id):
        return CustomerAddress.query.filter_by(user_id=user_id).all()

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
