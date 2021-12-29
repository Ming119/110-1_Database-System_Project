from app.controllers.indexController import *
from flask import Blueprint

bp = Blueprint('index', __name__)

bp.route('/', methods=['GET', 'POST'])(index)
bp.route('/register', methods=['GET', 'POST'])(register)
bp.route('/register/<token>', methods=['GET'])(confirmRegistration)
bp.route('/forgotPassword', methods=['GET', 'POST'])(forgotPassword)
bp.route('/resetPassword/<token>', methods=['GET', 'POST'])(resetPassword)
bp.route('/login', methods=['GET', 'POST'])(login)
bp.route('/logout', methods=['GET'])(logout)
bp.route('/shoppingCart', methods=['GET', 'POST'])(shoppingCart)
