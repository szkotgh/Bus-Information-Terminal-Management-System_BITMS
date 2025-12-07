from flask import Blueprint, g
from middleware.auth import terminal_auth_token_required
import modules.utils as utils
from modules.extensions import csrf
import db.domain.screen_show as db_screen_show

bp = Blueprint('terminal', __name__, url_prefix='/terminal')
csrf.exempt(bp)

@bp.route('', methods=['GET'])
@terminal_auth_token_required
def index():
    return utils.ResultDTO(200, g.terminal.message, data=dict(g.terminal.data)).to_response()

@bp.route('/screen_preset', methods=['GET'])
@terminal_auth_token_required
def get_screen_preset():
    screen_preset_list_result = db_screen_show.get_screen_show_by_terminal_id(g.terminal.data['id'])
    if not screen_preset_list_result.success:
        return utils.ResultDTO(400, f"조회에 실패했습니다: {screen_preset_list_result.message}").to_response()
    
    for index, screen_show in enumerate(screen_preset_list_result.data):
        if not screen_show['is_active']:
            screen_preset_list_result.data.pop(index)
    return utils.ResultDTO(200, screen_preset_list_result.message, data=screen_preset_list_result.data).to_response()