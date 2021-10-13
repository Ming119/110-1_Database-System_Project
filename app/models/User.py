from util import bcrypt, db, login
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous import SignatureExpired, BadSignature
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

    confirm = db.Column(db.Boolean, default=False)

    last_login  = db.Column(db.DateTime, nullable=True)
    create_at   = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

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

    def create_confirm_token(self, expires_in=900):
        """
        Generate a token from itsdangerous for confirm user's register
        :param expires_in: expiration time in seconds
        :return: token refer to user's id
        """

        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.user_id})

    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token: token
        :return: 回傳驗證是否正確，正確為True
        """

        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # validate
        except SignatureExpired:  # trigger SignatureExpired Error when token expires
            User.User.query.filter_by(user_id=data.get('user_id')).delete()
            return -1
        except BadSignature:  # trigger BadSignature Error when token wrong
            return -2
        finally:
            return self.user_id

    def __repr__(self):
        return '<User %r>' % (
            self.user_id,
            self.email,
            self.username,
            self.password_hash,
            self.first_name,
            self.last_name,
            self.confirm,
            self.create_at,
            self.modified_at
        )
