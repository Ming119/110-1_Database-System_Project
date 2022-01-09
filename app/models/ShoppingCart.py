from app.util import db
from datetime import datetime
from app.models.Product import Product
from app.models.Discount import ProductDiscount



class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.user_id'), primary_key=True)
    # cartItmes   = db.relationship('CartItem', backref='shopping_cart')

    amount = db.Column(db.Float(), nullable=False, default=0)

    @staticmethod
    def getByID(customer_id):
        return ShoppingCart.query.filter_by(customer_id=customer_id).first()




class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_id    = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False, default=0)
    amount   = db.Column(db.Float(), nullable=False, default=0)

    def update(self, quantity=None, amount=None):
        try:
            self.quantity = quantity or self.quantity
            self.amount   = amount or self.amount

            db.session.commit()
            return True

        except: return False

    def remove(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def create(cart_id, product_id, quantity, amount):
        if (quantity < 1):
            return False
        try:
            db.session.add(CartItem(
                        cart_id    = cart_id,
                        product_id = product_id,
                        quantity   = quantity,
                        amount     = amount
                ))
            db.session.commit()
            return True

        except: return False

    @staticmethod
    def getByID(cart_id, product_id):
        return CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()

    @staticmethod
    def getAllJoinedItems(user_id):
        return CartItem.query.join(
                    Product, CartItem.product_id==Product.product_id
                ).add_columns(
                    CartItem.cart_id, CartItem.quantity, CartItem.amount, Product.name, Product.description, Product.price, Product.product_id
                ).filter(CartItem.cart_id==user_id).join(
                    ProductDiscount, Product.discount_code==ProductDiscount.discount_code, isouter=True
                ).add_columns(
                    ProductDiscount.discountPercentage
                ).all()
