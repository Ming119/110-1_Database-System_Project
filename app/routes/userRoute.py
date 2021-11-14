from flask import Blueprint
from app.controllers.userController import (
    manageUsers, profile, deleteProfile
)

bp = Blueprint('user', __name__, url_prefix='/user')

bp.route('/', methods=['GET'])(manageUsers)
bp.route('/<int:user_id>', methods=['GET', 'POST'])(profile)
bp.route('/deleteProfile/<int:user_id>', methods=['GET'])(deleteProfile)
