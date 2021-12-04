from app.controllers.userController import *
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')                # MMS path prefix

bp.route('/', methods=['GET'])(index)                               # Index page of MMS
bp.route('/create/<role>', methods=['GET', 'POST'])(createUser)     # Create
bp.route('/<int:user_id>', methods=['GET', 'POST'])(profile)        # Read
bp.route('/edit/<int:user_id>', methods=['GET'])(editProfile)       # Upate
bp.route('/delete/<int:user_id>', methods=['GET'])(deleteProfile)   # Delete
