from flask import Blueprint;
from controllers.userController import profile;

user_bp = Blueprint('user', __name__, url_prefix='/user');

user_bp.route('/<int:uid>', methods=['GET'])(profile);
