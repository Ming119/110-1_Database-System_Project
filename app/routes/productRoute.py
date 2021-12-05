from app.controllers.productController import *
from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/product')                      # PMS path prefix

bp.route('/', methods=['GET', 'POST'])(index)                                   # Index page for PMS
bp.route('/<int:product_id>', methods=['GET', 'POST'])(details)                 # Read
bp.route('/deleteCategory/<int:category_id>', methods=['GET'])(deleteCategory)  # Delete category
bp.route('/deleteProduct/<int:product_id>', methods=['GET'])(deleteProduct)     # Delete product
