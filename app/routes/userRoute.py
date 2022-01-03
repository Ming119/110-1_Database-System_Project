from app.controllers.userController import *
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')                # MMS path prefix

bp.route('/', methods=['GET', 'POST'])(index)                       # Index page of MMS
bp.route('/filter/<role>', methods=['GET', 'POST'])(filterIndex)   # Filter index page of MMS
bp.route('/create/<role>', methods=['GET', 'POST'])(create)         # Create
bp.route('/<int:user_id>', methods=['GET'])(profile)                # Read
bp.route('/update/<int:user_id>', methods=['GET', 'POST'])(update)  # Update
bp.route('/changePassword/<int:user_id>', methods=['GET', 'POST'])(changePassword)
bp.route('/activate/<int:user_id>', methods=['GET'])(activate)
bp.route('/deactivate/<int:user_id>', methods=['GET'])(deactivate)
