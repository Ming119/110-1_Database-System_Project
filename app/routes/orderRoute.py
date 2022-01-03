from app.controllers.orderController import *
from flask import Blueprint

bp = Blueprint('order', __name__, url_prefix='/order', template_folder='templates/order')

bp.route('/', methods=['GET', 'POST'])(index)
bp.route('/filter/<int:order_id>', methods=['GET', 'POST'])(filterIndex)
bp.route('/<int:order_id', methods=['GET'])(details)
bp.route('/update/<int:order_id', methods=['GET'])(update)
