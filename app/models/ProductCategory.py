from util import db;
from datetime import datetime;

class ProductCategory(db.Model):
    __tablename__ = 'product_category';

    category_id = db.Column(db.Integer, primary_key=True);

    product_id = db.relationship('Product', backref='product_category');

    name        = db.Column(db.String(63),  nullable=False, unique=True);
    description = db.Column(db.String(255), nullable=True);
    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now);
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now);
    deleted_at  = db.Column(db.DateTime, nullable=True);

    def __repr__(self):
        return '<Category {}, {}, {}, {}, {}, {}, {}>'.format(
                    self.category_id,
                    self.product_id,
                    self.name,
                    self.description,
                    self.create_at,
                    self.modified_at,
                    self.deleted_at
                );
