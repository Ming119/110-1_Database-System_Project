from app.db import db;
from datetime import datetime;

class ProductInventory(db.Model):
    __tablename__ = 'product_inventory';

    inventory_id = db.Column(db.Integer, primary_key=True);

    product_id = db.relationship('Product', backref='product_inventory', uselist=False);

    quantity    = db.Column(db.Integer,  nullable=False, default=0);
    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now);
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now);
    deleted_at  = db.Column(db.DateTime, nullable=True);

    def __repr__(self):
        return '<Inventory %r>' %(
                    self.inventory_id,
                    self.product_id,
                    self.quantity,
                    self.create_at,
                    self.modified_at,
                    self.deleted_at
                );
