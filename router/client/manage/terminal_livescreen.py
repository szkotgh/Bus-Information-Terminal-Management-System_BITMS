from flask import Blueprint, render_template, request
import db.domain.terminal as db_terminal
from middleware.auth import login_required
import modules.utils as utils
import modules.constants as constants

bp = Blueprint('terminal_livescreen', __name__, url_prefix='/terminal_livescreen')

@bp.route('', methods=['GET'])
@login_required
def index():
    terminal_list_result = db_terminal.get_terminal_list()
    return render_template('manage/terminal/livescreen.html', terminal_list=terminal_list_result)