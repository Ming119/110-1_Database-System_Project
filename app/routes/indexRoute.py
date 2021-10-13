from flask import Blueprint
from controllers.indexController import (
    index, register, confirmRegistration, login, logout
)

bp = Blueprint('index', __name__)

bp.route('/', methods=['GET'])(index)
bp.route('/register', methods=['GET', 'POST'])(register);
bp.route('/register/<token>', methods=['GET', 'POST'])(confirmRegistration);
bp.route('/login', methods=['GET', 'POST'])(login);
bp.route('/logout', methods=['GET'])(logout);
