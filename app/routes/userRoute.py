from app.controllers.userController import *
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')                # MMS path prefix

bp.route('/', methods=['GET'])(index)                               # Index page of MMS
bp.route('/filter/<role>', methods=['GET', 'POST'])(filter_index)           # Filter index page of MMS
bp.route('/create/<role>', methods=['GET', 'POST'])(create)         # Create
bp.route('/<int:user_id>', methods=['GET'])(profile)                # Read
bp.route('/update/<int:user_id>', methods=['GET', 'POST'])(update)  # Update
bp.route('/activate/<int:user_id>', methods=['GET'])(activate)
bp.route('/deactivate/<int:user_id>', methods=['GET'])(deactivate)
