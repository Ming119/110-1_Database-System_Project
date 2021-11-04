from flask import Blueprint
from app.controllers.userController import profile, manageUsers

bp = Blueprint('user', __name__, url_prefix='/user')

bp.route('/<int:user_id>', methods=['GET'])(profile)
bp.route('/manageUsers', methods=['GET'])(manageUsers)
