from datetime import timedelta
import os
from flask import Blueprint, g, request
from middleware.auth import terminal_auth_token_required
from modules.extensions import csrf
import modules.utils as utils
import requests

from router.client.manage import everline

bp = Blueprint('everline', __name__, url_prefix='/everline')

csrf.exempt(bp)

@bp.route('/train', methods=['GET'])
@terminal_auth_token_required
def train():
    print("A")
    try:
        res = requests.get(f"{os.environ['EVERLINE_API_SERVER']}/api/train")
        res.raise_for_status()
        
        res_json = res.json()
        
        api_message = res_json.get('message')
        api_data = res_json.get('data')
        
        if api_data is None:
            raise Exception("Data Not Found")
        
        return utils.ResultDTO(200, api_message, api_data, True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(500, str(f"EVERLINE_API_SERVER_ERROR: {e}"), success=False).to_response()

@bp.route('/station', methods=['GET'])
@terminal_auth_token_required
def station():
    print("A")
    try:
        res = requests.get(f"{os.environ['EVERLINE_API_SERVER']}/api/station")
        res.raise_for_status()
        
        res_json = res.json()
        
        api_message = res_json.get('message')
        api_data = res_json.get('data')
        
        if api_data is None:
            raise Exception("Data Not Found")
        
        return utils.ResultDTO(200, api_message, api_data, True).to_response()
        
    except Exception as e:
        return utils.ResultDTO(500, str(f"EVERLINE_API_SERVER_ERROR: {e}"), success=False).to_response()