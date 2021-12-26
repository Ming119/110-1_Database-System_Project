from app.controllers.userController import *
from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')                # MMS path prefix

bp.route('/', methods=['GET'])(index)                               # Index page of MMS
bp.route('/create/<role>', methods=['GET', 'POST'])(create)         # Create
bp.route('/<int:user_id>', methods=['GET'])(profile)                # Read
bp.route('/update/<int:user_id>', methods=['GET', 'POST'])(update)  # Update
bp.route('/active/<int:user_id>', methods=['GET'])(active)
bp.route('/deactive/<int:user_id>', methods=['GET'])(deactive)
