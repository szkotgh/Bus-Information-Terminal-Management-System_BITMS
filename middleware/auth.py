from flask import request, redirect, url_for, session, flash, g
import functools
import modules.utils as utils
import modules.constants as constants
import db.domain.terminal as db_terminal
import db.domain.session as db_session
from modules.extensions import socketio

# Terminal Socket
def socket_token_or_login_required(f):
    @functools.wraps(f) 
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization'): # Token Auth
            return socket_token_required(f)(*args, **kwargs)

        if 'session_id' in session: # Web Login Auth
            return login_required(f)(*args, **kwargs)
        
        socketio.emit('connect_error', {'message': 'unauthorized'}, room=request.sid) # Unauthorized
        return False
    return decorated_function

def socket_token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            socketio.emit('connect_error', {'message': 'unauthorized'}, room=request.sid)
            return False
        
        auth_token = utils.extract_bearer_token(auth_token)
        if not auth_token:
            socketio.emit('connect_error', {'message': 'Bearer token is invalid.'}, room=request.sid)
            return False
        
        terminal_result = db_terminal.get_terminal_by_auth_token(auth_token)
        if not terminal_result.success:
            socketio.emit('connect_error', {'message': terminal_result.message}, room=request.sid)
            return False
        if not terminal_result.data['status'] == constants.STATUS_ACTIVE:
            socketio.emit('connect_error', {'message': "Status is not active."}, room=request.sid)
            return False
        g.terminal = terminal_result.data
        return f(*args, **kwargs)
    return decorated_function

def socket_token_required_ignore_status(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            socketio.emit('connect_error', {'message': 'unauthorized'}, room=request.sid)
            return False
        
        auth_token = utils.extract_bearer_token(auth_token)
        if not auth_token:
            socketio.emit('connect_error', {'message': 'Bearer token is invalid.'}, room=request.sid)
            return False
        
        terminal_result = db_terminal.get_terminal_by_auth_token(auth_token)
        if not terminal_result.success:
            socketio.emit('connect_error', {'message': terminal_result.message}, room=request.sid)
            return False
        g.terminal = terminal_result.data
        return f(*args, **kwargs)
    return decorated_function

# Terminal Web API
def terminal_auth_token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return utils.ResultDTO(code=401, message='인증 헤더가 없습니다.').to_response()
        
        auth_token = utils.extract_bearer_token(request.headers['Authorization'])
        if not auth_token:
            return utils.ResultDTO(code=401, message='Bearer 토큰이 유효하지 않습니다.').to_response()
        
        terminal_result = db_terminal.get_terminal_by_auth_token(auth_token)
        if not terminal_result.success:
            return utils.ResultDTO(code=401, message=f"인증 실패: {terminal_result.message}").to_response()
        
        if not terminal_result.data['status'] == constants.STATUS_ACTIVE:
            return utils.ResultDTO(code=401, message="비활성화된 장치입니다.").to_response()
        
        g.terminal = terminal_result
        return f(*args, **kwargs)
        
    return decorated_function


# Web Session
def check_login_session(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_id' not in session:
            return f(*args, **kwargs)
        
        return login_required(f)(*args, **kwargs)
    return decorated_function

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_id' not in session:
            session.clear()
            flash('로그인 후 작업하십시오.', 'warning')
            return redirect(url_for('router.client.login'))
        
        session_result = db_session.get_session_by_session_id(session.get('session_id'))
        if not session_result.success:
            session.clear()
            flash('다시 로그인하십시오.', 'error')
            return redirect(url_for('router.client.login'))
        
        if session_result.data['status'] == constants.STATUS_INACTIVE:
            session.clear()
            flash('만료된 세션입니다. 다시 로그인하십시오.', 'error')
            return redirect(url_for('router.client.login'))
        if session_result.data['status'] == constants.STATUS_BLOCKED:
            session.clear()
            flash('차단된 세션입니다. 다시 로그인하십시오.', 'error')
            return redirect(url_for('router.client.login'))
        
        expected_checksum = utils.create_session_checksum_from_request()
        if session_result.data['checksum'] != expected_checksum:
            db_session.block_session_by_session_id(session.get('session_id'))
            session.clear()
            flash('유효하지 않은 세션입니다. 다시 로그인하십시오.', 'error')
            return redirect(url_for('router.client.login'))
        
        g.session = session_result
        return f(*args, **kwargs)
    return decorated_function

def not_login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_id' in session:
            return redirect(url_for('router.client.index'))
        return f(*args, **kwargs)
    return decorated_function
