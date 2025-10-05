from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('', methods=['GET'])
def index():
    return "API Endpoint", 200