from flask import Blueprint;
from controllers.productController import (
    index, details, delete
);

bp = Blueprint('product', __name__, url_prefix='/product');

bp.route('/', methods=['GET', 'POST'])(index);
bp.route('/<int:product_id>', methods=['GET', 'POST'])(details);
bp.route('/delete', methods=['POST'])(delete);
