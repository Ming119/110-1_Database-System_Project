from app.util import db
from datetime import datetime
from app.models.User import Customer
from app.models.CustomerAddress import CustomerAddress
from app.models.Product import Product
from app.models.Comment import Comment


class Order(db.Model):
    __tablename__ = 'order'

    order_id       = db.Column(db.Integer, primary_key=True)
    customer_id    = db.Column(db.Integer,   db.ForeignKey('customer.user_id'),             nullable=False)
    address_id     = db.Column(db.Integer,   db.ForeignKey('customer_address.address_id'),  nullable=False)
    order_discount = db.Column(db.String(8), db.ForeignKey('order_discount.discount_code'), nullable=True)
    orderItems     = db.relationship('OrderItem', backref='order')

    amount      = db.Column(db.Float(),  nullable=False, default=0)
    shippingFee = db.Column(db.Integer,  nullable=False, default=0)
    shipDate    = db.Column(db.DateTime, nullable=True)
    status      = db.Column(db.String(16),  nullable=False, default='processing')

    payment_type = db.Column(db.String(8),  nullable=True)
    provider     = db.Column(db.String(64), nullable=True)
    account_no   = db.Column(db.Integer,    nullable=True)

    create_at = db.Column(db.DateTime, default=datetime.now)

    def process(self):
        try:
            if self.status == 'processing':
                self.status = 'delivering'
            elif self.status == 'delivering':
                self.status = 'delivered'
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def joinUserAndAddress():
        return db.session.query(Order, Customer, CustomerAddress).filter(
                    Order.customer_id==Customer.user_id, Order.address_id==CustomerAddress.address_id
                )

    @staticmethod
    def joinProduct():
        return db.session.query(Order).join(
                OrderItem, Order.order_id == OrderItem.order_id
            ).add_columns(
                OrderItem.quantity, OrderItem.amount
            ).join(
                Product, OrderItem.product_id == Product.product_id
            ).add_columns(
                Product.name, Product.price
            ).join(
                Comment, Order.customer_id == Comment.user_id, isouter=True
            ).add_columns(
                Comment.rating, Comment.comment
            )

        return db.session.query(Order, OrderItem, Product, Comment).filter(
                    Order.order_id       == OrderItem.order_id,
                    OrderItem.product_id == Product.product_id,
                    OrderItem.product_id == Comment.product_id,
                    Comment.user_id      == Order.customer_id
                    )
                # ).join(Comment, Comment.user_id == Order.customer_id, isouter=True).filter(
                #
                # )

    @staticmethod
    def getOrderProduct(order_id):
        return Order.joinProduct().filter(Order.order_id==order_id).all()

    @staticmethod
    def getAll():
        return Order.joinUserAndAddress().all()

    @staticmethod
    def getAllContains(word):
        return Order.joinUserAndAddress().filter(
            db.or_(Customer.email.contains(word), Customer.username.contains(word),
                    Customer.first_name.contains(word), Customer.last_name.contains(word),
                    CustomerAddress.country.contains(word), CustomerAddress.city.contains(word),
                    CustomerAddress.address.contains(word), CustomerAddress.postal_code.contains(word),
                    CustomerAddress.telephone.contains(word),
            )).all()

    @staticmethod
    def getByStatus(status):
        return Order.joinUserAndAddress().filter(Order.status==status).all()

    @staticmethod
    def getByID(order_id):
        return Order.joinUserAndAddress().filter(Order.order_id==order_id).first()

    @staticmethod
    def getByCustomerID(customer_id, status=None):
        if status:
            return Order.joinUserAndAddress().filter(Order.customer_id==customer_id, Order.status==status).all()
        return Order.joinUserAndAddress().filter(Order.customer_id==customer_id).all()

    @staticmethod
    def count(status=None, customer_id=None):
        if status and customer_id:
            return Order.query.filter_by(status=status, customer_id=customer_id).count()

        if status:
            return Order.query.filter_by(status=status).count()

        return Order.query.count()

    @staticmethod
    def create(customer_id, address_id, order_discount, items, amount, shippingFee, payment_type='Cash', provider=None, account_no=None):
        try:
            order = Order(
                        customer_id    = customer_id,
                        address_id     = address_id,
                        order_discount = order_discount,
                        amount         = amount,
                        shippingFee    = shippingFee,
                        payment_type   = payment_type
            )
            if order.payment_type == 'Credit':
                order.provider = provider
                order.account_no = account_no

            db.session.add(order)
            db.session.commit()
            for item in items:
                db.session.add(OrderItem(
                                order_id   = order.order_id,
                                product_id = item.product_id,
                                quantity   = item.quantity,
                                amount     = item.amount
                            ))

            db.session.commit()
            return True
        except: return False



class OrderItem(db.Model):
    __tablename__ = 'order_item'

    order_id   = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), primary_key=True)

    quantity = db.Column(db.Integer, nullable=False, default=0)
    amount   = db.Column(db.Float(), nullable=False, default=0)
