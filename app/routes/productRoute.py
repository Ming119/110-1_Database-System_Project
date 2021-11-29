from app.controllers import *
from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/product')

bp.route('/', methods=['GET', 'POST'])(index)
bp.route('/<int:product_id>', methods=['GET', 'POST'])(details)
bp.route('/deleteCategory/<int:category_id>', methods=['GET'])(deleteCategory)
bp.route('/deleteProduct/<int:product_id>', methods=['GET'])(deleteProduct)
