from app.controllers.discountController import *
from flask import Blueprint

bp = Blueprint('discount', __name__, url_prefix='/discount')    # DMS path prefix

bp.route('/', methods=['GET'])(index)                           # Index page of DMS
bp.route('/create', methods=['GET', 'POST'])(create)            # Create
bp.route('/<discount_code>', methods=['GET'])(details)          # Read
bp.route('/update/<discount_code>', methods=['GET', 'POST'])(update)    # Update
