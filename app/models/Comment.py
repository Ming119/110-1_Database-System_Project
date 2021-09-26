from util import db;
from datetime import datetime;

class Comment(db.Model):
    __tablename__ = 'comments';
    cid           = db.Column(db.Integer, primary_key=True, nullable=False);
    pid           = db.relationship('');
    uid           = db.relationship('User', backref='comments');
    date          = db.Column(db.Date, default=datetime.now, unique=False, nullable=False);
    comment       = db.Column(db.String(64), unique=False, nullable=True);
    rate          = db.Column(db.Ineeger, unique=False, nullable=False);

    def __repr__(self):
        return '<comment: %r>' %(self.cid, self.pid, self.uid, self.date, self.comment, self.rate);
