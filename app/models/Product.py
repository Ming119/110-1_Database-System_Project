from app.db import db;

class Product(db.Model):
    __tablename__ = 'products';
    pid           = db.Column(db.Integer, primary_key=True);
    name          = db.Column(db.String(64), unique=True);
    users         = db.relationship('User', backref='product', lazy='dynamic') # 外键关系，动态更新

    def __repr__(self): # 相当于toString
        return '<product %r>' %self.name
