from app.util import db
from datetime import datetime

class Discount(db.Model):
    __tablename__ = 'discount'

    discount_code = db.Column(db.String(8), primary_key=True)
    product_id    = db.relationship('Product', backref='discount')

    description      = db.Column(db.String(255), nullable=True)
    type             = db.Column(db.String(255), nullable=False)

    start_at    = db.Column(db.DateTime, default=datetime.now)
    end_at      = db.Column(db.DateTime, nullable=True)
    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    __mapper_args__ = {
        'polymorphic_identity':'discount',
        'polymorphic_on':type
    }

    def update(self, code=None, description=None, start_at=None, end_at=None):
        try:
            self.discount_code = code or self.discount_code
            self.description = description or self.description
            self.start_at = start_at or self.start_at
            self.end_at = end_at or self.end_at
            db.session.commit()
            return True

        except: return False

    def is_active(self):
        return ((self.start_at < datetime.now()) and (self.end_at > datetime.now()))

    @staticmethod
    def getAll():
        return Discount.query.all()

    @staticmethod
    def getByCode(code):
        return Discount.query.filter_by(discount_code=code).first()

    @staticmethod
    def getByType(type):
        return Discount.query.filter_by(type=type).all()

    @staticmethod
    def count(type=None):
        if type:
            return Discount.query.filter_by(type=type).count()

        return Discount.query.count()

    def __repr__(self):
        return '<Discount {}, {}, {}, {}, {}, {}>'.format(
            self.discount_code,
            self.description,
            self.start_at,
            self.end_at,
            self.create_at,
            self.modified_at,
        )



class ShippingDiscount(Discount):
    __tablename__   = 'shipping_discount'
    __mapper_args__ = {
        'polymorphic_identity':'shipping',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)

    atLeastAmount = db.Column(db.Float(), nullable=False)

    def update(self, code=None, description=None, start_at=None, end_at=None, atLeastAmount=None):
        if super().update(code, description, start_at, end_at):
            try:
                self.atLeastAmount = atLeastAmount or self.atLeastAmount
                db.session.commit()
                return True

            except: return False
        return False

    @staticmethod
    def create(discount_code, start_at, end_at, atLeastAmount, description=None, type='shipping'):
        try:
            db.session.add(ShippingDiscount(
                discount_code = discount_code,
                description   = description,
                type          = type,
                start_at      = start_at,
                end_at        = end_at,
                atLeastAmount = atLeastAmount
            ))
            db.session.commit()
            return True

        except: return False

    @staticmethod
    def getActive():
        return ShippingDiscount.query.filter(Discount.start_at<datetime.now(), Discount.end_at>datetime.now()).order_by(ShippingDiscount.atLeastAmount).first()



class ProductDiscount(Discount):
    __tablename__   = 'product_discount'
    __mapper_args__ = {
        'polymorphic_identity':'product',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)
    product_id    = db.relationship('Product', backref='product_discount')

    discountPercentage = db.Column(db.Integer, nullable=False)

    def update(self, code=None, description=None, start_at=None, end_at=None, discountPercentage=None):
        if super().update(code, description, start_at, end_at):
            try:
                self.discountPercentage = discountPercentage or self.discountPercentage
                db.session.commit()
                return True

            except: return False
        return False

    @staticmethod
    def create(discount_code, start_at, end_at, discountPercentage, description=None, type='product'):
        try:
            db.session.add(ProductDiscount(
                discount_code      = discount_code,
                description        = description,
                type               = type,
                start_at           = start_at,
                end_at             = end_at,
                discountPercentage = discountPercentage
            ))
            db.session.commit()
            return True

        except: return False



class OrderDiscount(Discount):
    __tablename__   = 'order_discount'
    __mapper_args__ = {
        'polymorphic_identity':'order',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)

    discountPercentage = db.Column(db.Integer, nullable=False)
    atLeastAmount      = db.Column(db.Float(), nullable=False)

    def update(self, code=None, description=None, start_at=None, end_at=None, discountPercentage=None, atLeastAmount=None):
        if super().update(code, description, start_at, end_at):
            try:
                self.discountPercentage = discountPercentage or self.discountPercentage
                self.atLeastAmount = atLeastAmount or self.atLeastAmount
                db.session.commit()
                return True

            except: return False
        return False

    @staticmethod
    def create(discount_code, start_at, end_at, discountPercentage, atLeastAmount, description=None, type='order'):
        try:
            db.session.add(OrderDiscount(
                discount_code      = discount_code,
                description        = description,
                type               = type,
                start_at           = start_at,
                end_at             = end_at,
                discountPercentage = discountPercentage,
                atLeastAmount      = atLeastAmount
            ))
            db.session.commit()
            return True

        except: return False
