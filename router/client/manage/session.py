from flask import Blueprint, render_template, request, redirect, url_for, session
import db.domain.session as db_session
from middleware.auth import login_required
import modules.utils as utils

bp = Blueprint('session', __name__, url_prefix='/session')

@bp.route('', methods=['GET'])
@login_required
def index():
    user_session_id = session.get('session_id')
    session_list = db_session.get_session_list()
    return render_template('manage/session/index.html', session_list=session_list, user_session_id=user_session_id)

@bp.route('', methods=['DELETE'])
@login_required
def deactivate():
    id = request.json.get('id')
    if not id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()
    
    deactivate_result = db_session.deactivate_session_by_id(id)
    if not deactivate_result.success:
        return utils.ResultDTO(code=400, message=deactivate_result.message).to_response()
    return utils.ResultDTO(code=200, message=deactivate_result.message).to_response()

@bp.route('/all', methods=['DELETE'])
@login_required
def deactivate_all():
    deactivate_result = db_session.deactivate_all_sessions()
    if not deactivate_result.success:
        return utils.ResultDTO(code=400, message=deactivate_result.message).to_response()
    return utils.ResultDTO(code=200, message=deactivate_result.message).to_response()