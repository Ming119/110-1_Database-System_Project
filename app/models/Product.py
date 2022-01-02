from app.util import db
from datetime import datetime
from app.models.ProductCategory import ProductCategory
from app.models.Discount import ProductDiscount

class Product(db.Model):
    __tablename__ = 'product'

    product_id    = db.Column(db.Integer, primary_key=True)
    category_id   = db.Column(db.Integer,   db.ForeignKey('product_category.category_id'),   nullable=False)
    discount_code = db.Column(db.String(8), db.ForeignKey('product_discount.discount_code'), nullable=True)
    comments      = db.relationship('Comment', backref='product')

    name        = db.Column(db.String(63),  nullable=False)
    description = db.Column(db.String(255), nullable=True)
    image_url   = db.Column(db.String(255), nullable=False)
    price       = db.Column(db.Float(),     nullable=False)
    quantity    = db.Column(db.Integer,     nullable=False)

    is_active = db.Column(db.Boolean,  default=True, nullable=False)

    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def update(self, category_id, discount_code=None, name=None, description=None, price=None, quantity=None):
        self.category_id = category_id or self.category_id
        self.discount_code = discount_code or self.discount_code
        self.name        = name or self.name
        self.description = description or self.description
        self.price       = price or self.price
        self.quantity    = quantity or self.quantity
        db.session.commit()

    @staticmethod
    def create(category_id, name, price, quantity, image_url, description=None):
        prodcuct = Product.query.filter_by(name=name).first()
        if prodcuct is None:
            db.session.add(Product(
                            category_id = category_id,
                            name        = name,
                            description = description,
                            price       = price,
                            quantity    = quantity,
                            image_url   = image_url
                          ))
            db.session.commit()
            return True

        elif not product.is_active:
            prodcut.update(category_id, name, price, quantity, description)
            return True

        else:
            return False

    @staticmethod
    def getAll():
        return Product.query.all()

    @staticmethod
    def getAllWithoutInactive():
        return Product.query.filter_by(is_active=True).all()

    @staticmethod
    def getAllJoinedProduct(is_active=None):
        if is_active is not None:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(Product.is_active==is_active).all()
        else:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).all()

    @staticmethod
    def getAllJoinedProductByCategoryID(category_id, is_active=None):
        if is_active is not None:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(
                Product.category_id==category_id, Product.is_active==is_active
            ).all()
        else:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(
                Product.category_id==category_id
            ).all()

    @staticmethod
    def getAllJoinedProductContains(word, is_active=None):
        if is_active is not None:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(
                Product.name.contains(word), Product.is_active==is_active
            ).all()
        else:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(
                Product.name.contains(word)
            ).all()

    @staticmethod
    def getAllJoinedProductByCategoryIDContains(category_id, word, is_active=None):
        if is_active is not None:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(
                Product.category_id==category_id, Product.name.contains(word), Product.is_active==is_active
            ).all()
        else:
            return db.session.query(
                Product, ProductCategory, ProductDiscount
            ).join(ProductCategory).join(ProductDiscount, isouter=True).filter(
                Product.category_id==category_id, Product.name.contains(word)
            ).all()

    @staticmethod
    def getByCategoryID(category_id):
        return Product.query.filter_by(category_id=category_id).all()

    @staticmethod
    def getByCategoryIDWithoutInactive(category_id):
        return Product.query.filter_by(category_id=category_id, is_active=True).all()

    @staticmethod
    def getByID(product_id):
        return Product.query.filter_by(product_id=product_id).first()

    @staticmethod
    def getByIDWithoutInactive(product_id):
        return Product.query.filter_by(product_id=product_id, is_active=True).first()

    @staticmethod
    def getByName(name):
        return Product.query.filter_by(name=name).first()

    @staticmethod
    def publishByID(product_id):
        try:
            product  = Product.getByID(product_id)
            category = ProductCategory.getByIDWithoutInactive(product.category_id)
            if category is None: return False
            product.is_active = True
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def withholdByID(product_id):
        try:
            product = Product.getByIDWithoutInactive(product_id)
            product.is_active = False
            db.session.commit()
            return True
        except: return False

    def __repr__(self):
        return '<Product {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
                    self.product_id,
                    self.category_id,
                    self.name,
                    self.description,
                    self.price,
                    self.quantity,
                    self.is_active,
                    self.create_at,
                    self.modified_at,
                )
