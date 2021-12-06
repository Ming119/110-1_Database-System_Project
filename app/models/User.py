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

    email         = db.Column(db.String(63),   nullable=False, unique=True)
    username      = db.Column(db.String(31),   nullable=False, unique=True)
    password_hash = db.Column(db.String(1023), nullable=False)
    first_name    = db.Column(db.String(31),   nullable=False)
    last_name     = db.Column(db.String(31),   nullable=False)
    role          = db.Column(db.String(15),   nullable=False)
    # icon          = db.Column(db.BLOB,         nullable=False)

    last_login  = db.Column(db.DateTime, nullable=True)
    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    delete_at   = db.Column(db.DateTime, nullable=True)

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

    def update(self, username=None, first_name=None, last_name=None):
        try:
            self.username   = username or self.username
            self.first_name = first_name or self.first_name
            self.last_name  = last_name or self.last_name
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def getAll():
        return User.query.filter(User.delete_at==None).all()

    @staticmethod
    def getByID(user_id):
        return User.query.filter(User.user_id==user_id, User.delete_at==None).first()

    @staticmethod
    def getByEmail(email):
        return User.query.filter(User.email==email, User.delete_at==None).first()

    @staticmethod
    def getByUsername(username):
        return User.query.filter(User.username==username, User.delete_at==None).first()

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

    userPayment  = db.relationship('CustomerPayment', backref='customer')
    userAddress  = db.relationship('CustomerAddress', backref='customer')
    orderHistory = db.relationship('Order',           backref='customer')

    confirm = db.Column(db.Boolean,  default=False)
    DOB     = db.Column(db.Date)

    def create_confirm_token(self, expires_in=300):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.user_id})

    def validate_confirm_token(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            return None

        return data

    def update(self, username=None, first_name=None, last_name=None, DOB=None):
        try:
            super().update(username, first_name, last_name)
            self.DOB = DOB or self.DOB
            db.session.commit()
            return True
        except: return False

    def updateConfirm(self, flag):
        try:
            self.confirm = flag
            db.session.commit()
            return True
        except: return False

    @staticmethod
    def create(email, username, password, first_name, last_name, DOB):
        try:
            customer = Customer(
                            email      = email,
                            username   = username,
                            password   = password,
                            first_name = first_name,
                            last_name  = last_name,
                            DOB        = DOB
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
                        last_name  = last_name,
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
                        last_name  = last_name,
                        )
            db.session.add(admin)
            db.session.commit()
            return User.getByUsername(admin.username)
        except:
            return None

    def deleteUserByID(user_id):
        try:
            user = User.getByID(user_id)
            if (user.role == 'admin'): return False
            user.delete_at = datetime.now()
            db.session.commit()
            return True

        except: return False
