from flask import Blueprint
from controllers.productController import (
    index, details, edit, delete
);

bp = Blueprint('product', __name__, url_prefix='/product')

bp.route('/', methods=['GET', 'POST'])(index);
bp.route('/<int:product_id>', methods=['GET'])(details);
bp.route('/edit/<int:product_id>', methods=['POST'])(edit);
bp.route('/delete', methods=['POST'])(delete);
