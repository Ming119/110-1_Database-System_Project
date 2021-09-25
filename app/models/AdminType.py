from app.db import db;
from datetime import datetime;

class AdminType(db.Model):
    __tablename__ = 'admin_type';

    type_id = db.Column(db.Integer, primary_key=True);

    admin_type = db.Column(db.String(15), nullable=False);
    permissions = db.Column(db.String(255), nullable=False);

    create_at   = db.Column(db.DateTime, nullable=False, default=datetime.now);
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now);

    def __repr__(self):
        return '<AdminType %r>' %(
                    self.type_id,
                    self.admin_type,
                    self.permissions,
                    self.create_at,
                    self.modified_at,
                );
