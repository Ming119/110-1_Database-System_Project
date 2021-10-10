from flask import Blueprint;
from controllers.manageUserController import manageUsers;

bp = Blueprint('manageUser', __name__, url_prefix='/manageUsers');

bp.route('/<int:user_id>', methods=['GET'])(manageUsers);
