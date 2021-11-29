from app.controllers import *
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')

bp.route('/', methods=['GET'])(manageUsers)
bp.route('/create', methods=['GET', 'POST'])(createNewUser)
bp.route('/<int:user_id>', methods=['GET', 'POST'])(profile)
bp.route('/edit/<int:user_id>', methods=['GET'])(editProfile)
bp.route('/delete/<int:user_id>', methods=['GET'])(deleteProfile)
