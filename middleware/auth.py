import functools
from flask import request, redirect, url_for, session, flash
import modules.utils as utils

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_login' not in session:
            flash('로그인하세요.', 'warning')
            return redirect(url_for('router.client.login'))
        
        print(f"ip: {utils.get_client_ip()}, user_agent: {request.headers.get('User-Agent', '')}")
        expected_checksum = utils.create_session_checksum_from_request()
        if session.get('checksum') != expected_checksum:
            session.clear()
            flash('다시 로그인하세요.', 'error')
            return redirect(url_for('router.client.login'))
        return f(*args, **kwargs)
    return decorated_function

def not_login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_login' in session:
            return redirect(url_for('router.client.index'))
        return f(*args, **kwargs)
    return decorated_function