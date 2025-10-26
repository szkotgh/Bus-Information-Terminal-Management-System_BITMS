from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from middleware.auth import not_login_required, login_required, check_login_session
from . import manage
import os
import bcrypt
import modules.utils as utils
import db.domain.session as db_session
import db.domain.system_config as db_config

bp = Blueprint('client', __name__, url_prefix='/client')
bp.register_blueprint(manage.bp)

@bp.route('')
@check_login_session
def index():
    is_login = session.get('session_id', False)
    session_result = db_session.get_session_by_session_id(session.get('session_id'))
    login_ip = session_result.data['ip'] if session_result.success else None
    
    return render_template('index.html', is_login=is_login, login_ip=login_ip)

@bp.route('/login', methods=['GET', 'POST'])
@not_login_required
def login():
    if request.method == 'POST':
        input_pw = request.form.get('password')
        if not input_pw or not input_pw.strip():
            return render_template('login.html'), 400
        
        admin_password_result = db_config.get_config_by_key('admin_password')
        
        # set Default Password
        if not admin_password_result.success:
            env_password = os.environ.get('DEFAULT_PASSWORD')
            if not env_password:
                flash('비밀번호를 불러올 수 없습니다.', 'error')
                return render_template('login.html'), 500
            
            hashed_password = bcrypt.hashpw(env_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            result = db_config.create_kv('admin_password', hashed_password, 'login password for web admin client')
            if not result.success:
                flash(f"비밀번호 초기화에 실패했습니다: {result.message}", 'error')
                return render_template('login.html'), 500
            flash(f"비밀번호가 기본값으로 초기화되었습니다. 비밀번호를 변경하십시오.", 'success')
            stored_password_hash = hashed_password
        else:
            stored_password_hash = admin_password_result.data['config_value']
        
        if bcrypt.checkpw(input_pw.encode('utf-8'), stored_password_hash.encode('utf-8')): # type: ignore
            session_result = db_session.create_session(utils.get_client_ip(), utils.get_user_agent(), utils.create_session_checksum_from_request())
            if not session_result.success:
                flash(session_result.message, 'error')
                return render_template('login.html'), 500
            session.clear()
            session['session_id'] = session_result.data
            return redirect(url_for('router.client.index'))
        
        return render_template('login.html'), 401
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    db_session.deactivate_session_by_session_id(session.get('session_id'))
    session.clear()
    return redirect(url_for('router.client.index'))