from flask import Blueprint, redirect
from . import api, client

bp = Blueprint('router', __name__)
bp.register_blueprint(api.bp)
bp.register_blueprint(client.bp)

@bp.route('/')
def index():
    return redirect('/client')