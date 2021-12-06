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
    deleted_at  = db.Column(db.DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity':'discount',
        'polymorphic_on':type
    }

    def __repr__(self):
        return '<Discount %r>' % (
            self.discount_code,
            self.name,
            self.description,
            self.is_active,
            self.create_at,
            self.modified_at,
            self.deleted_at
        )



class ShippingDiscount(Discount):
    __tablename__   = 'shipping_discount'
    __mapper_args__ = {
        'polymorphic_identity':'shipping_discount',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)

    atLeastAmount = db.Column(db.Integer, nullable=False)



class ProductDiscount(Discount):
    __tablename__   = 'product_discount'
    __mapper_args__ = {
        'polymorphic_identity':'product_discount',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)
    product_id    = db.relationship('Product', backref='product_discount')

    discountPresentage = db.Column(db.Float(), nullable=False)



class CategoryDiscount(Discount):
    __tablename__   = 'category_discount'
    __mapper_args__ = {
        'polymorphic_identity':'category_discount',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)
    category_id   = db.relationship('ProductCategory', backref='category_discount')

    discountPresentage = db.Column(db.Float(), nullable=False)
