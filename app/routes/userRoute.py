from app.controllers.userController import *
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')                        # MMS path prefix

bp.route('/', methods=['GET'])(index)                                       # Index page of MMS
bp.route('/create/<role>', methods=['GET', 'POST'])(createNewUser)          # Create
bp.route('/<int:user_id>', methods=['GET', 'POST'])(profile)                # Read
bp.route('/update/<int:user_id>', methods=['GET', 'POST'])(updateProfile)   # Upate
bp.route('/delete/<int:user_id>', methods=['GET'])(deleteProfile)           # Delete
