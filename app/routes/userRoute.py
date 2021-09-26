from flask import Blueprint;
from controllers.userController import profile;

bp = Blueprint('user', __name__, url_prefix='/user');

bp.route('/<int:uid>', methods=['GET'])(profile);
