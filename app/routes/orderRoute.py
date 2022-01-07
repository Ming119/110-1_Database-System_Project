from app.controllers.orderController import *
from flask import Blueprint

bp = Blueprint('order', __name__, url_prefix='/order')

bp.route('/<int:user_id>', methods=['GET', 'POST'])(index)
bp.route('/filter/<int:user_id>', methods=['GET', 'POST'])(filterIndex)
bp.route('/<int:order_id>', methods=['GET'])(details)
bp.route('/update/<int:order_id>', methods=['GET'])(update)
