from flask import Blueprint, request, render_template, flash, redirect, url_for
from middleware.auth import login_required
import modules.utils as utils
import db.domain.system_config as db_config
import db.domain.session as db_session
import bcrypt

bp = Blueprint('password', __name__, url_prefix='/manage/password')

@bp.route('', methods=['GET'])
@login_required
def index():
    return render_template('manage/password/index.html')

@bp.route('', methods=['POST'])
@login_required
def update():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_password or not new_password or not confirm_password:
        flash('누락된 값을 확인하십시오.', 'error')
        return render_template('manage/password/index.html')
    
    if new_password != confirm_password:
        flash('비밀번호 확인이 올바르지 않습니다.', 'error')
        return render_template('manage/password/index.html')
    
    password_validation = utils.is_valid_password(new_password)
    if not password_validation.success:
        flash(f"새로운 비밀번호가 유효하지 않습니다: {password_validation.detail}", 'error')
        return render_template('manage/password/index.html')
    
    admin_password_result = db_config.get_config_by_key('admin_password')
    if not admin_password_result.success:
        flash('비밀번호를 불러올 수 없습니다.', 'error')
        return render_template('manage/password/index.html')
    
    stored_password_hash = admin_password_result.data['config_value']
    
    if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password_hash.encode('utf-8')):
        flash('현재 비밀번호가 올바르지 않습니다.', 'error')
        return render_template('manage/password/index.html')
    
    # Update Password
    new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    save_result = db_config.update_kv('admin_password', new_password_hash, 'login password for web admin client')
    if not save_result.success:
        flash(f'비밀번호 변경 중 오류가 발생했습니다: {save_result.message}', 'error')
        return render_template('manage/password/index.html')
    
    flash('비밀번호가 성공적으로 변경되었습니다.', 'success')
    db_session.deactivate_all_sessions()
    return redirect(url_for('router.client.index'))
