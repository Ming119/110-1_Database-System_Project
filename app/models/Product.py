from util import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'

    product_id  = db.Column(db.Integer, primary_key=True)

    category_id  = db.Column(db.Integer, db.ForeignKey('product_category.category_id'), nullable=False)
    discount_id  = db.relationship('Discount', backref='product')

    name        = db.Column(db.String(63),  nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price       = db.Column(db.Float(),     nullable=False)
    quantity    = db.Column(db.Integer(),   nullable=False)

    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at  = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Product {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
                    self.product_id,
                    self.category_id,
                    self.discount_id,
                    self.name,
                    self.description,
                    self.price,
                    self.quantity,
                    self.create_at,
                    self.modified_at,
                    self.deleted_at
                )
