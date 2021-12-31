from app.controllers.discountController import *
from flask import Blueprint

bp = Blueprint('discount', __name__, url_prefix='/discount')    # DMS path prefix

bp.route('/', methods=['GET', 'POST'])(index)                           # Index page of DMS
bp.route('/filter/<type>', methods=['GET', 'POST'])(filterIndex)                           # Index page of DMS
bp.route('/create/<type>', methods=['GET', 'POST'])(create)            # Create
bp.route('/<discount_code>', methods=['GET'])(details)          # Read
bp.route('/update/<discount_code>', methods=['GET'])(update)    # Update
bp.route('/delete/<discount_code>', methods=['GET'])(delete)    # Delete
