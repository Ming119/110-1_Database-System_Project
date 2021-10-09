from util import db, bcrypt, login
from datetime import datetime
from flask_login import UserMixin
from models import Adminuser


class Adminuser(db.Model, UserMixin):
    __tablename__ = 'adminuser'

    user_id = db.Column(db.Integer, primary_key=True)

    # type_id = db.Column(db.Integer, db.ForeignKey('admin_type.type_id'), nullable=False)

    email         = db.Column(db.String(64),   nullable=False, unique=True)
    username      = db.Column(db.String(31),   nullable=False, unique=True)
    password_hash = db.Column(db.String(1023), nullable=False)
    first_name    = db.Column(db.String(31),   nullable=False)
    last_name     = db.Column(db.String(31),   nullable=False)
    admin_type    = db.Column(db.String(15),   nullable=False)

    last_login  = db.Column(db.DateTime, nullable=True)
    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def get_id(self):
        return self.user_id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Adminuser %r>' % (
            self.adminuser_id,
            self.type_id,
            self.email,
            self.username,
            self.password_hash,
            self.first_name,
            self.last_name,
            self.last_login,
            self.create_at,
            self.modified_at
        )
