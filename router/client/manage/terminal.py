from flask import Blueprint, render_template, request
import db.domain.terminal as db_terminal
from middleware.auth import login_required
import modules.utils as utils
import modules.constants as constants

bp = Blueprint('terminal', __name__, url_prefix='/terminal')

@bp.route('', methods=['GET'])
@login_required
def index():
    terminal_list_result = db_terminal.get_terminal_list()
    return render_template('manage/terminal/manage_terminal.html', terminal_list=terminal_list_result.data)

@bp.route('/list', methods=['GET'])
@login_required
def get_list():
    terminal_list_result = db_terminal.get_terminal_list()
    if not terminal_list_result.success:
        return utils.ResultDTO(code=400, message=f"조회에 실패했습니다: {terminal_list_result.message}").to_response()
    return utils.ResultDTO(code=200, message=terminal_list_result.message, data=terminal_list_result.data).to_json()

@bp.route('', methods=['POST'])
@login_required
def create():
    terminal_name = request.json.get('name')
    if not terminal_name:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    create_result = db_terminal.create_terminal(terminal_name, utils.generate_hash(16))
    if not create_result.success:
        return utils.ResultDTO(code=400, message=f"생성에 실패했습니다: {create_result.message}").to_response()
    return utils.ResultDTO(code=201, message=create_result.message).to_response()

@bp.route('', methods=['DELETE'])
@login_required
def delete():
    terminal_id = request.json.get('id')
    if not terminal_id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()
    delete_result = db_terminal.delete_terminal(terminal_id)
    if not delete_result.success:
        return utils.ResultDTO(code=400, message=f"삭제에 실패했습니다: {delete_result.message}").to_response()
    return utils.ResultDTO(code=200, message=delete_result.message).to_response()

@bp.route('', methods=['PUT'])
@login_required
def update():
    terminal_id = request.json.get('id')
    terminal_name = request.json.get('name')
    terminal_status = request.json.get('status')
    if not terminal_id or not terminal_name or not terminal_status:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()
    
    update_result = db_terminal.update_terminal(terminal_id, terminal_name, terminal_status)
    if not update_result.success:
        return utils.ResultDTO(code=400, message=f"업데이트에 실패했습니다: {update_result.message}").to_response()
    return utils.ResultDTO(code=200, message=update_result.message).to_response()

@bp.route('/update/auth_token', methods=['POST'])
@login_required
def update_auth_token():
    terminal_id = request.json.get('id')
    if not terminal_id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()
    
    update_result = db_terminal.update_terminal_auth_token(terminal_id)
    if not update_result.success:
        return utils.ResultDTO(code=400, message=f"업데이트에 실패했습니다: {update_result.message}").to_response()
    return utils.ResultDTO(code=200, message=update_result.message).to_response()