from flask import Blueprint
from controllers.userController import profile

bp = Blueprint('user', __name__, url_prefix='/user')

bp.route('/<int:user_id>', methods=['GET'])(profile)
