from app.util import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    cid        = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('customer.user_id'),   nullable=False)

    comment = db.Column(db.String(256), nullable=True)
    rating  = db.Column(db.Integer,     nullable=False)
    date    = db.Column(db.DateTime,    nullable=False, default=datetime.now)

    def __repr__(self):
        return '<comment: %r>' % (
            self.cid,
            self.pid,
            self.uid,
            self.date,
            self.comment,
            self.rate
        )
