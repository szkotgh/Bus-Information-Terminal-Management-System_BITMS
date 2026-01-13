from flask import Blueprint, render_template, request
from middleware.auth import login_required
import db.domain.screen_show as db_screen_show
import db.domain.terminal as db_terminal
import db.domain.screen_preset as db_screen_preset
import modules.utils as utils
import modules.constants as constants

bp = Blueprint('terminal_showmanage', __name__,
               url_prefix='/terminal_showmanage')


@bp.route('', methods=['GET'])
@login_required
def index():
    terminal_list_result = db_terminal.get_terminal_list()
    screen_preset_list_result = db_screen_preset.get_screen_preset_list()
    screen_show_list_result = db_screen_show.get_screen_show_list()
    return render_template('manage/terminal/manage_screen_show.html', terminal_list=terminal_list_result.data, screen_preset_list=screen_preset_list_result.data, screen_show_list=screen_show_list_result.data)


@bp.route('/list', methods=['GET'])
@login_required
def get_list_by_terminal_id():
    terminal_id = request.args.get('terminal_id')
    if not terminal_id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    screen_show_list_result = db_screen_show.get_screen_show_by_terminal_id(
        terminal_id)
    if not screen_show_list_result.success:
        return utils.ResultDTO(code=400, message=f"조회에 실패했습니다: {screen_show_list_result.message}").to_response()

    return utils.ResultDTO(code=200, message=screen_show_list_result.message, data=screen_show_list_result.data).to_response()


@bp.route('', methods=['POST'])
@login_required
def create():
    terminal_id = request.json.get('terminal_id')
    screen_preset_id = request.json.get('screen_preset_id')
    is_active = request.json.get('is_active')
    order_id = request.json.get('order_id')
    desc = request.json.get('desc')
    value1 = request.json.get('value1', '')
    value2 = request.json.get('value2', '')
    value3 = request.json.get('value3', '')
    value4 = request.json.get('value4', '')

    try:
        terminal_id = int(terminal_id) if terminal_id is not None else None
        screen_preset_id = int(
            screen_preset_id) if screen_preset_id is not None else None
        is_active = bool(is_active) if is_active is not None else None
        order_id = int(order_id) if order_id is not None else None
        desc = str(desc) if desc is not None else None
        value1 = str(value1) if value1 is not None else ''
        value2 = str(value2) if value2 is not None else ''
        value3 = str(value3) if value3 is not None else ''
        value4 = str(value4) if value4 is not None else ''
    except (ValueError, TypeError):
        return utils.ResultDTO(code=400, message='잘못된 데이터 타입입니다.').to_response()
    if not terminal_id or not screen_preset_id or is_active is None or not order_id or not desc:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    create_result = db_screen_show.create_screen_show(
        terminal_id, screen_preset_id, is_active, order_id, desc, value1, value2, value3, value4)
    if not create_result.success:
        return utils.ResultDTO(code=400, message=f"생성에 실패했습니다: {create_result.message}").to_response()
    return utils.ResultDTO(code=201, message=create_result.message).to_response()


@bp.route('', methods=['DELETE'])
@login_required
def delete():
    screen_show_id = request.json.get('id')
    if not screen_show_id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    delete_result = db_screen_show.delete_screen_show(screen_show_id)
    if not delete_result.success:
        return utils.ResultDTO(code=400, message=f"삭제에 실패했습니다: {delete_result.message}").to_response()
    return utils.ResultDTO(code=200, message=delete_result.message).to_response()


@bp.route('', methods=['PUT'])
@login_required
def update():
    screen_show_id = request.json.get('id')
    if not screen_show_id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    terminal_id = request.json.get('terminal_id')
    screen_preset_id = request.json.get('screen_preset_id')
    is_active = request.json.get('is_active')
    order_id = request.json.get('order_id')
    desc = request.json.get('desc')
    value1 = request.json.get('value1', '')
    value2 = request.json.get('value2', '')
    value3 = request.json.get('value3', '')
    value4 = request.json.get('value4', '')

    try:
        terminal_id = int(terminal_id) if terminal_id is not None else None
        screen_preset_id = int(
            screen_preset_id) if screen_preset_id is not None else None
        is_active = bool(is_active) if is_active is not None else None
        order_id = int(order_id) if order_id is not None else None
        desc = str(desc) if desc is not None else None
        value1 = str(value1) if value1 is not None else ''
        value2 = str(value2) if value2 is not None else ''
        value3 = str(value3) if value3 is not None else ''
        value4 = str(value4) if value4 is not None else ''
    except (ValueError, TypeError):
        return utils.ResultDTO(code=400, message='잘못된 데이터 타입입니다.').to_response()
    if not terminal_id or not screen_preset_id or is_active is None or not order_id or not desc:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    update_result = db_screen_show.update_screen_show(
        screen_show_id, terminal_id, screen_preset_id, is_active, order_id, desc, value1, value2, value3, value4)
    if not update_result.success:
        return utils.ResultDTO(code=400, message=f"수정에 실패했습니다: {update_result.message}").to_response()
    return utils.ResultDTO(code=200, message=update_result.message).to_response()
