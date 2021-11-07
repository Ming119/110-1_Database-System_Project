from app.util import db
from datetime import datetime

class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    category_id = db.Column(db.Integer, primary_key=True)
    product_id  = db.relationship('Product', backref='product_category')

    name        = db.Column(db.String(63),  nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at  = db.Column(db.DateTime, nullable=True)

    def update(self, name=None, description=None, deleted_at=None):
        self.name        = name or self.name
        self.description = description or self.description
        self.deleted_at  = deleted_at
        db.session.commit()

    @staticmethod
    def create(name, description=None):
        productCategory = ProductCategory.query.filter_by(name=name).first()
        if productCategory is None:
            db.session.add(ProductCategory(
                            name        = name,
                            description = description
                           ))
            db.session.commit()
            return True

        elif productCategory.deleted_at is not None:
            productCategory.update(name, description)
            return True

        else:
            return False

    @staticmethod
    def getAll():
        return ProductCategory.query.filter_by(deleted_at=None).all()

    @staticmethod
    def getByID(category_id):
        return ProductCategory.query.filter_by(category_id=category_id, deleted_at=None).first()

    @staticmethod
    def getByName(name):
        return ProductCategory.query.filter_by(name=name, deleted_at=None).first()

    @staticmethod
    def deleteByID(category_id):
        productCategory = ProductCategory.getByID(category_id)
        if productCategory.product_id:
            return False
        else:
            productCategory.deleted_at = datetime.now()
            db.session.commit()
            return True

    @staticmethod
    def deleteByName(name):
        productCategory = ProductCategory.getByName(category_id)
        if productCategory.product_id:
            return False

        else:
            productCategory.deleted_at = datetime.now()
            db.session.commit()
            return True

    def __repr__(self):
        return '<Category %r>' % (
            self.category_id,
            self.name,
            self.description,
            self.create_at,
            self.modified_at,
            self.deleted_at
        )
