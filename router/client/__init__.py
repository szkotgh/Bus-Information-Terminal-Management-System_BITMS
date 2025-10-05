from flask import Blueprint, redirect, render_template, request, session, url_for
from middleware.auth import not_login_required, login_required
from . import terminal
import os
import bcrypt
import modules.utils as utils

bp = Blueprint('client', __name__, url_prefix='/client')
bp.register_blueprint(terminal.bp)

@bp.route('')
def index():
    is_login = session.get('is_login', False)
    
    return render_template('index.html', is_login=is_login)

@bp.route('/login', methods=['GET', 'POST'])
@not_login_required
def login():
    if request.method == 'POST':
        input_pw = request.form.get('password')
        if not input_pw or not input_pw.strip():
            return render_template('login.html'), 400
        
        if bcrypt.checkpw(input_pw.encode('utf-8'), os.environ['ADMIN_PASSWORD'].encode('utf-8')):
            session.clear()
            session['is_login'] = True
            session['checksum'] = utils.create_session_checksum_from_request()
            return redirect(url_for('router.client.index'))
        
        return render_template('login.html'), 401
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('router.client.index'))