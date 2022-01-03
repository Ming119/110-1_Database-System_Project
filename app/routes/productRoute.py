from app.controllers.productController import *
from flask import Blueprint

bp = Blueprint('product', __name__, url_prefix='/product')                      # PMS path prefix

bp.route('/', methods=['GET', 'POST'])(index)                                   # Index page for PMS
bp.route('/filter/<int:category_id>', methods=['GET', 'POST'])(filterIndex)     # Filter index page for PMS
bp.route('/<int:product_id>', methods=['GET', 'POST'])(details)                 # Read
bp.route('/withholdCategory/<int:category_id>', methods=['GET'])(withholdCategory)  # Delete category
bp.route('/publishCategory/<int:category_id>', methods=['GET'])(publishCategory)  # Delete category
bp.route('/withholdProduct/<int:product_id>', methods=['GET'])(withholdProduct)   # Delete product
bp.route('/publishProduct/<int:product_id>', methods=['GET'])(publishProduct)    # Delete product
