from util import db
from datetime import datetime

class Discount(db.Model):
    __tablename__ = 'discount'

    discount_id      = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)

    name             = db.Column(db.String(64),  nullable=False)
    code             = db.Column(db.String(8),   nullable=False, unique=True)
    description      = db.Column(db.String(255), nullable=True)
    discount_percent = db.Column(db.Float,       nullable=False, default=1.0)
    active           = db.Column(db.Boolean,     nullable=False, default=False)

    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at  = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Discount {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
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
