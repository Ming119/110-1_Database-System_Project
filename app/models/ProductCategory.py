from app.util import db
from datetime import datetime

class ProductCategory(db.Model):
    __tablename__ = 'product_category'

    category_id   = db.Column(db.Integer, primary_key=True)
    product_id    = db.relationship('Product', backref='product_category')
    discount_code = db.Column(db.String(8), db.ForeignKey('category_discount.discount_code'), nullable=True)

    name        = db.Column(db.String(63),  nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    is_active   = db.Column(db.Boolean, default=True, nullable=False)

    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def update(self, name=None, description=None):
        self.name        = name or self.name
        self.description = description or self.description
        self.is_active   = True 
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

        elif not productCategory.is_active:
            productCategory.update(name, description)
            return True

        else:
            return False

    @staticmethod
    def getAll():
        return ProductCategory.query.filter_by(is_active=True).all()

    @staticmethod
    def getByID(category_id):
        return ProductCategory.query.filter_by(category_id=category_id, is_active=True).first()

    @staticmethod
    def getByName(name):
        return ProductCategory.query.filter_by(name=name, is_active=True).first()

    @staticmethod
    def deleteByID(category_id):
        productCategory = ProductCategory.getByID(category_id)
        if productCategory.product_id:
            return False
        else:
            productCategory.is_active = False
            db.session.commit()
            return True

    @staticmethod
    def deleteByName(name):
        productCategory = ProductCategory.getByName(category_id)
        if productCategory.product_id:
            return False

        else:
            productCategory.is_active = False
            db.session.commit()
            return True

    def __repr__(self):
        return '<Category %r>' % (
            self.category_id,
            self.name,
            self.description,
            self.is_active,
            self.create_at,
            self.modified_at,
        )
