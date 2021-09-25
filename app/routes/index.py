from flask import Blueprint, session, g;
from controllers.indexcontroller import (
    index, register, login, logout
);

bp = Blueprint('index', __name__);

bp.route('/', methods=['GET'])(index)
bp.route('/register', methods=['GET', 'POST'])(register);
bp.route('/login', methods=['GET','POST'])(login);
bp.route('/logout', methods=['POST'])(logout);

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id');

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
