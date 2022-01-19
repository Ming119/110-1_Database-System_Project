from app.controllers.report_controller import *
from flask import Blueprint

bp = Blueprint('report', __name__, url_prefix='/report')

bp.route('/', methods=['GET', 'POST'])(index)
