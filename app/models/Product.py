from app.util import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'

    product_id  = db.Column(db.Integer, primary_key=True)

    category_id  = db.Column(db.Integer, db.ForeignKey('product_category.category_id'), nullable=False)
    # discount_id  = db.relationship('discount', backref='product')

    name        = db.Column(db.String(63),  nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price       = db.Column(db.Float(),     nullable=False)
    quantity    = db.Column(db.Integer(),   nullable=False)

    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at  = db.Column(db.DateTime, nullable=True)

    def update(self, category_id, name=None, description=None, price=None, quantity=None, deleted_at=None):
        self.category_id = category_id or self.category_id
        self.name        = name or self.name
        self.description = description or self.description
        self.price       = price or self.price
        self.quantity    = quantity or self.quantity
        self.deleted_at  = deleted_at
        db.session.commit()

    @staticmethod
    def create(category_id, name, price, quantity, description=None):
        prodcuct = Product.query.filter_by(name=name).first()
        if prodcuct is None:
            db.session.add(Product(
                            category_id = category_id,
                            name        = name,
                            description = description,
                            price       = price,
                            quantity    = quantity
                          ))
            db.session.commit()
            return True

        elif product.deleted_at is not None:
            prodcut.update(category_id, name, price, quantity, description)
            return True

        else:
            return False

    @staticmethod
    def getAll():
        return Product.query.filter_by(deleted_at=None).all()

    @staticmethod
    def getByID(product_id):
        return Product.query.filter_by(product_id=product_id, deleted_at=None).first()

    @staticmethod
    def getByName(name):
        return Product.query.filter_by(name=name, deleted_at=None).first()

    @staticmethod
    def deleteByID(product_id):
        product = Product.getByID(product_id)
        product.deleted_at = datetime.now()
        db.session.commit()
        return True

    @staticmethod
    def deleteByName(name):
        product = Product.getByName(name)
        product.deleted_at = datetime.now()
        db.session.commit()
        return True

    def __repr__(self):
        return '<Product {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
                    self.product_id,
                    self.category_id,
                    self.name,
                    self.description,
                    self.price,
                    self.quantity,
                    self.create_at,
                    self.modified_at,
                    self.deleted_at
                )
