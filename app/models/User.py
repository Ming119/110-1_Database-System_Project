from app.db import db;

class User(db.Model):
    __tablename__ = 'users'
    uid           = db.Column(db.Integer, primary_key=True);
    userName      = db.Column(db.String(64), unique=False);
    firstName     = db.Column(db.String(64), unique=False);
    lastName      = db.Column(db.String(64), unique=False);
    phoneNumber   = db.Column(db.String(64), unique=True);
    email         = db.Column(db.String(64), unique=True);
    address       = db.Column(db.String(64), unique=True);

    # users         = db.relationship('User', backref='role', lazy='dynamic');

    def __repr__(self):
        return '<Role %r>' %self.userName
