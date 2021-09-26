from flask import Blueprint, session, g;
from controllers.indexController import (
    index, register, confirmRegistration, login, logout
);
from models import User;


bp = Blueprint('index', __name__);

bp.route('/', methods=['GET'])(index)
bp.route('/register', methods=['GET', 'POST'])(register);
bp.route('/register/<token>', methods=['GET'])(confirmRegistration);
bp.route('/login', methods=['GET', 'POST'])(login);
bp.route('/logout', methods=['GET'])(logout);

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id');

    if user_id is None:
        g.user = None
    else:
        g.user = User.User.query.filter_by(user_id=user_id).first();
