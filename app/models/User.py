from app.util import db, bcrypt, login
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from flask import current_app
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id       = db.Column(db.Integer, primary_key=True)
    cartItmes   = db.relationship('CartItem', backref='user')

    email         = db.Column(db.String(64),   nullable=False, unique=True)
    username      = db.Column(db.String(32),   nullable=False, unique=True)
    password_hash = db.Column(db.String(1024), nullable=False)
    first_name    = db.Column(db.String(32),   nullable=False)
    last_name     = db.Column(db.String(32),   nullable=False)
    role          = db.Column(db.String(16),   nullable=False)

    is_active   = db.Column(db.Boolean, nullable=False, default=True)

    last_login  = db.Column(db.DateTime, nullable=True)
    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.now,
                            onupdate=datetime.now
                        )

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':role
    }

    # Override for @login.user_loader
    def get_id(self):
        return self.user_id

    @property   # Private attribute
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter    # Mapping password to password_hash
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def update(self, username=None, first_name=None, last_name=None, is_active=None):
        try:
            self.username   = username or self.username
            self.first_name = first_name or self.first_name
            self.last_name  = last_name or self.last_name
            self.is_active  = is_active or self.is_active
            db.session.commit()
            return True
        except: return False

    def changePassword(self, password):
        try:
            self.password = password
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def getAll(is_active=None):
        if is_active:
            return User.query.filter_by(is_active=True).all()

        return User.query.all()

    @staticmethod
    def getByID(user_id, is_active=None):
        if is_active:
            return User.query.filter_by(user_id=user_id, is_active=is_active).first()

        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def getByEmail(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def getByUsername(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def getByRole(role):
        return User.query.filter(User.role==role).all()

    @staticmethod
    def count(type=None):
        if type:
            return User.query.filter_by(role=type).count()

        return User.query.count()

    def __repr__(self):
        return '<User {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(
                    self.user_id,
                    self.email,
                    self.username,
                    self.password_hash,
                    self.first_name,
                    self.last_name,
                    self.last_login,
                    self.create_at,
                    self.modified_at
                )



# Inherited from User
class Customer(User):
    __tablename__   = 'customer'
    __mapper_args__ = {
        'polymorphic_identity':'customer',
    }

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

    # userPayment  = db.relationship('CustomerPayment', backref='customer')
    userAddress  = db.relationship('CustomerAddress', backref='customer')
    orderHistory = db.relationship('Order',           backref='customer')
    comments     = db.relationship('Comment',         backref='customer')

    DOB     = db.Column(db.Date,    nullable=False)

    def create_confirm_token(self, expires_in=300):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.user_id})

    def create_order_token(self, order_id, expires_in=604800):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.user_id, 'order_id': order_id})

    def validate_confirm_token(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            return None

        return data

    def update(self, username=None, first_name=None, last_name=None, is_active=None, DOB=None):
        try:
            super().update(username, first_name, last_name, is_active)
            self.DOB = DOB or self.DOB
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def create(email, username, password, first_name, last_name, DOB, is_active=False):
        try:
            customer = Customer(
                            email      = email,
                            username   = username,
                            password   = password,
                            first_name = first_name,
                            last_name  = last_name,
                            DOB        = DOB,
                            is_active  = is_active
                       )
            db.session.add(customer)
            db.session.commit()

            return User.getByUsername(customer.username)
        except: return None



# Inherited from User
class Staff(User):
    __tablename__   = 'staff'
    __mapper_args__ = {
        'polymorphic_identity':'staff',
    }

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

    @staticmethod
    def create(email, username, password, first_name, last_name):
        try:
            staff = Staff(
                        email      = email,
                        username   = username,
                        password   = password,
                        first_name = first_name,
                        last_name  = last_name
                    )
            db.session.add(staff)
            db.session.commit()

            return User.getByUsername(staff.username)
        except:
            return None



# Inherited from User
class Admin(User):
    __tablename__   = 'admin'
    __mapper_args__ = {
        'polymorphic_identity':'admin',
    }

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

    @staticmethod
    def create(email, username, password, first_name, last_name):
        try:
            admin = Admin(
                        email      = email,
                        username   = username,
                        password   = password,
                        first_name = first_name,
                        last_name  = last_name
                        )
            db.session.add(admin)
            db.session.commit()
            return User.getByUsername(admin.username)
        except:
            return None

    def activateUserByID(self, user_id):
        try:
            user = User.getByID(user_id)
            user.is_active = True
            db.session.commit()
            return True

        except: return False

    def deactivateUserByID(self, user_id):
        try:
            user = User.getByID(user_id, True)
            if (user.role == 'admin'): return False
            user.is_active = False
            db.session.commit()
            return True

        except: return False
