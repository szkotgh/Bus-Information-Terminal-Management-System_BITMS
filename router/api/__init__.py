from flask import Blueprint, g
import modules.utils as utils
from middleware.auth import terminal_auth_token_required
from modules.extensions import csrf
from . import terminal, bus, everline, weather

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(terminal.bp)
bp.register_blueprint(bus.bp)
bp.register_blueprint(everline.bp)
bp.register_blueprint(weather.bp)

csrf.exempt(bp)

@bp.route('', methods=['GET'])
@terminal_auth_token_required
def index():
    return utils.ResultDTO(code=200, message=f"Terminal Authenticated", data=dict(g.terminal.data)).to_response()