from flask import Blueprint, render_template
from middleware.auth import login_required

bp = Blueprint('weather', __name__, url_prefix='/weather')

@bp.route('', methods=['GET'])
@login_required
def index():
    return render_template('manage/api/weather.html')
