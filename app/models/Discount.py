from app.util import db
from datetime import datetime

class Discount(db.Model):
    __tablename__ = 'discount'

    discount_code = db.Column(db.String(8), primary_key=True)

    name             = db.Column(db.String(64),  nullable=False)
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

    def update(self, name=None, description=None, start_at=None, end_at=None):
        try:
            self.name = name or self.name
            self.description = description or self.description
            self.start_at = start_at or self.start_at
            self.end_at = end_at or self.end_at
            db.session.commit()
            return True

        except: return False


    @staticmethod
    def getAll():
        return Discount.query.all()

    @staticmethod
    def getAllWithoutInactive():
        return Discount.query.filter_by(is_active=True).all()

    @staticmethod
    def delete(discount_code):
        try:
            db.session.delete(Discount.getByID(discount_code))
            db.session.commit()
            return True

        except: return False



    def __repr__(self):
        return '<Discount %r>' % (
            self.discount_code,
            self.name,
            self.description,
            self.is_active,
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

    def update(self, name=None, description=None, start_at=None, end_at=None, atLeastAmount=None):
        if super().update(name, description, start_at, end_at):
            try:
                self.atLeastAmount = atLeastAmount or self.atLeastAmount
                db.session.commit()
                return True

            except: return False
        return False

    @staticmethod
    def create(discount_code, name, type, start_at, end_at, atLeastAmount, description=None):
        try:
            db.session.add(Discount(
                discount_code = discount_code,
                name          = name,
                description   = description,
                type          = type,
                start_at      = start_at,
                end_at        = end_at,
                atLeastAmount = atLeastAmount
            ))
            db.session.commit()
            return True

        except: return False



class ProductDiscount(Discount):
    __tablename__   = 'product_discount'
    __mapper_args__ = {
        'polymorphic_identity':'product',
    }

    discount_code = db.Column(db.String(8), db.ForeignKey('discount.discount_code'), primary_key=True)
    product_id    = db.relationship('Product', backref='product_discount')

    discountPercentage = db.Column(db.Float(), nullable=False)

    def update(self, name=None, description=None, start_at=None, end_at=None, discountPercentage=None):
        if super().update(name, description, start_at, end_at):
            try:
                self.discountPercentage = discountPercentage or self.discountPercentage
                db.session.commit()
                return True

            except: return False
        return False

    @staticmethod
    def create(discount_code, name, type, start_at, end_at, discountPercentage, description=None):
        try:
            db.session.add(Discount(
                discount_code      = discount_code,
                name               = name,
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

    discountPercentage = db.Column(db.Float(), nullable=False)
    atLeastAmount      = db.Column(db.Float(), nullable=False)

    def update(self, name=None, description=None, start_at=None, end_at=None, discountPercentage=None, atLeastAmount=None):
        if super().update(name, description, start_at, end_at):
            try:
                self.discountPercentage = discountPercentage or self.discountPercentage
                self.atLeastAmount = atLeastAmount or self.atLeastAmount
                db.session.commit()
                return True

            except: return False
        return False

    @staticmethod
    def create(discount_code, name, type, start_at, end_at, discountPercentage, atLeastAmount, description=None):
        try:
            db.session.add(Discount(
                discount_code      = discount_code,
                name               = name,
                description        = description,
                type               = type,
                start_at           = start_at,
                end_at             = end_at,
                discountPercentage = discountPercentage
                atLeastAmount      = atLeastAmount
            ))
            db.session.commit()
            return True

        except: return False
