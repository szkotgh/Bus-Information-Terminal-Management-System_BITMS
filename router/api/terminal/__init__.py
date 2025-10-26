from flask import Blueprint
from middleware.auth import terminal_auth_token_required
import modules.utils as utils
bp = Blueprint('terminal', __name__, url_prefix='/terminal')

@bp.route('', methods=['GET'])
def index():
    return utils.ResultDTO(200, "Terminal API Endpoint").to_response()