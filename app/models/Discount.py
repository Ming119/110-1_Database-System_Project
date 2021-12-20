from app.util import db
from datetime import datetime

class Discount(db.Model):
    __tablename__ = 'discount'

    discount_code = db.Column(db.String(8), primary_key=True)

    name             = db.Column(db.String(64),  nullable=False)
    description      = db.Column(db.String(255), nullable=True)
    type             = db.Column(db.String(255), nullable=False)

    start_at    = db.Column(db.DateTime, default=datetime.now)
    end_at      = db.Column(db.DateTime, nullable=True)
    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    __mapper_args__ = {
        'polymorphic_identity':'discount',
        'polymorphic_on':type
    }

    @staticmethod
    def getAll():
        return Discount.query.all()

    @staticmethod
    def getAllWithoutInactive():
        return Discount.query.filter_by(is_active=True).all()

    def __repr__(self):
        return '<Discount %r>' % (
            self.discount_code,
            self.name,
            self.description,
            self.is_active,
            self.create_at,
            self.modified_at,
        )



class ShippingDiscount(Discount):
    __tablename__   = 'shipping_discount'
    __mapper_args__ = {
        'polymorphic_identity':'shipping',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)

    atLeastAmount = db.Column(db.Float(), nullable=False)



class ProductDiscount(Discount):
    __tablename__   = 'product_discount'
    __mapper_args__ = {
        'polymorphic_identity':'product',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)
    product_id    = db.relationship('Product', backref='product_discount')

    discountPercentage = db.Column(db.Float(), nullable=False)



class OrderDiscount(Discount):
    __tablename__   = 'order_discount'
    __mapper_args__ = {
        'polymorphic_identity':'order',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)

    discountPercentage = db.Column(db.Float(), nullable=False)
    atLeastAmount      = db.Column(db.Float(), nullable=False)
