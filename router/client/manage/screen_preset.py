from flask import Blueprint, render_template, request
from middleware.auth import login_required
import db.domain.screen_preset as db_screen_preset
import modules.utils as utils

bp = Blueprint('screen_preset', __name__, url_prefix='/screen_preset')

@bp.route('', methods=['GET'])
@login_required
def index():
    screen_preset_list_result = db_screen_preset.get_screen_preset_list()
    return render_template('manage/terminal/manage_screen_preset.html', screen_preset_list=screen_preset_list_result.data)

@bp.route('', methods=['POST'])
@login_required
def create():
    name = request.json.get('name')
    command = request.json.get('command')
    value_desc = request.json.get('value_desc')
    if not name or not command or not value_desc:
        return utils.ResultDTO(code=400, message="누락된 값을 확인하십시오.").to_response()
    
    create_result = db_screen_preset.create_screen_preset(name, command, value_desc)
    if not create_result.success:
        return utils.ResultDTO(code=400, message=f"생성에 실패했습니다: {create_result.message}").to_response()
    return utils.ResultDTO(code=201, message=create_result.message).to_response()

@bp.route('/list', methods=['GET'])
@login_required
def get_list_by_terminal_id():
    list_result = db_screen_preset.get_screen_preset_list()
    if not list_result.success:
        return utils.ResultDTO(code=400, message=f"조회에 실패했습니다: {list_result.message}").to_response()
    return utils.ResultDTO(code=200, message=list_result.message, data=list_result.data).to_response()

@bp.route('', methods=['DELETE'])
@login_required
def delete():
    id = request.json.get('id')
    if not id:
        return utils.ResultDTO(code=400, message="누락된 값을 확인하십시오.").to_response()
    
    delete_result = db_screen_preset.delete_screen_preset(id)
    if not delete_result.success:
        return utils.ResultDTO(code=400, message=f"삭제에 실패했습니다: {delete_result.message}").to_response()
    return utils.ResultDTO(code=200, message=delete_result.message).to_response()

@bp.route('', methods=['PUT'])
@login_required
def update():
    id = request.json.get('id')
    name = request.json.get('name')
    command = request.json.get('command')
    value_desc = request.json.get('value_desc')
    if not id or not name or not command or not value_desc:
        return utils.ResultDTO(code=400, message="누락된 값을 확인하십시오.").to_response()
    
    update_result = db_screen_preset.update_screen_preset(id, name, command, value_desc)
    if not update_result.success:
        return utils.ResultDTO(code=400, message=f"업데이트에 실패했습니다: {update_result.message}").to_response()
    return utils.ResultDTO(code=200, message=update_result.message).to_response()