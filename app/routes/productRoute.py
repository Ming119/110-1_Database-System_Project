from flask import Blueprint;
from controllers.productController import (
    index, search, details, edit, create, delete
);

bp = Blueprint('product', __name__, url_prefix='/product');

bp.route('/', methods=['GET', 'POST'])(index);
bp.route('/search', methods=['POST'])(search);
bp.route('/<int:product_id>', methods=['GET'])(details);
bp.route('/edit/<int:product_id>', methods=['POST'])(edit);
bp.route('/create', methods=['POST'])(create);
bp.route('/delete', methods=['POST'])(delete);
