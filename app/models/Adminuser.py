from util import db;
from datetime import datetime;

class Adminuser(db.Model):
    __tablename__ = 'adminuser';

    adminuser_id = db.Column(db.Integer, primary_key=True);

    type_id = db.Column(db.Integer, db.ForeignKey('admin_type.type_id'), nullable=False);

    email         = db.Column(db.String(64),   nullable=False, unique=True);
    username      = db.Column(db.String(31),   nullable=False, unique=True);
    password_hash = db.Column(db.String(1023), nullable=False);
    first_name    = db.Column(db.String(31),   nullable=False);
    last_name     = db.Column(db.String(31),   nullable=False);

    last_login  = db.Column(db.DateTime, nullable=True);
    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now);
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now);

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute');

    @password.setter
    def password(self, password):
        self.password_hash = Bcrypt.generate_password_hash(password).decode('utf8');

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password);

    def __repr__(self):
        return '<Adminuser %r>' %(
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
                );
