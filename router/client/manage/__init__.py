from flask import Blueprint
from . import terminal, station, terminal_livescreen, session, terminal_status, terminal_showmanage, weather, everline, screen_preset, password

bp = Blueprint('manage', __name__, url_prefix='/manage')
bp.register_blueprint(screen_preset.bp)
bp.register_blueprint(session.bp)
bp.register_blueprint(terminal.bp)
bp.register_blueprint(terminal_livescreen.bp)
bp.register_blueprint(terminal_showmanage.bp)
bp.register_blueprint(terminal_status.bp)
bp.register_blueprint(station.bp)
bp.register_blueprint(weather.bp)
bp.register_blueprint(everline.bp)
bp.register_blueprint(password.bp)