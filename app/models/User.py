from app.db import db;
from datetime import datetime;

class User(db.Model):
    __tablename__ = 'user';

    user_id       = db.Column(db.Integer, primary_key=True);

    email         = db.Column(db.String(64),   nullable=False, unique=True);
    username      = db.Column(db.String(31),   nullable=False, unique=True);
    password      = db.Column(db.String(1023), nullable=False);
    first_name    = db.Column(db.String(31),   nullable=False);
    last_name     = db.Column(db.String(31),   nullable=False);

    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now);
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now);

    def __repr__(self):
        return '<User %r>' %(
                    self.user_id,
                    self.email,
                    self.username,
                    self.password,
                    self.first_name,
                    self.last_name,
                    self.create_at,
                    self.modified_at
                );
