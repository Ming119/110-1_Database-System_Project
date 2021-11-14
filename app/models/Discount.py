from app.util import db
from datetime import datetime

class Discount(db.Model):
    __tablename__ = 'discount'

    discount_code = db.Column(db.String(8), primary_key=True)

    # product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)

    name             = db.Column(db.String(64),  nullable=False)

    description      = db.Column(db.String(255), nullable=True)
    discount_percent = db.Column(db.Float,       nullable=False, default=1.0)
    is_active        = db.Column(db.Boolean,     nullable=False, default=False)

    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at  = db.Column(db.DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity':'discount',
        # 'polymorphic_on':role
    }

    def __repr__(self):
        return '<Discount %r>' % (
            self.category_id,
            self.product_id,
            self.name,
            self.code,
            self.description,
            self.discount_percent,
            self.active,
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
