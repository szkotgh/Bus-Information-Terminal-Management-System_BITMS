from flask import Blueprint, g, request
from middleware.auth import terminal_auth_token_required
from modules.extensions import csrf
import modules.utils as utils
from dotenv import load_dotenv
import requests
import os
load_dotenv()

bp = Blueprint('weather', __name__, url_prefix='/weather')

csrf.exempt(bp)

@bp.route('', methods=['GET'])
def index():
    return utils.ResultDTO(200, "Weather API Endpoint").to_response()

@bp.route('/weather', methods=['GET'])
@terminal_auth_token_required
def weather():
    lat = request.args.get('y')
    lon = request.args.get('x')
    if not lat or not lon:
        return utils.ResultDTO(400, "Required parameters are missing").to_response()
    
    data = {
        "lat": lat,
        "lon": lon,
        "mode": "json",
        "units": "metric",
        "lang": "kr",
        "appid": os.environ['OPENWEATHERMAP_APPID'],
    }
    try:
        result = requests.get("https://api.openweathermap.org/data/2.5/weather", params=data)
        result = result.json()
    except Exception as e:
        return utils.ResultDTO(500, f"Internal Server Error: {e}").to_response()

    return utils.ResultDTO(200, "OK", data=result).to_response()

@bp.route('/airpollution', methods=['GET'])
@terminal_auth_token_required
def airpollution():
    lat = request.args.get('y')
    lon = request.args.get('x')
    if not lat or not lon:
        return utils.ResultDTO(400, "Required parameters are missing").to_response()

    data = {
        "lat": lat,
        "lon": lon,
        "appid": os.environ['OPENWEATHERMAP_APPID'],
    }
    try:
        result = requests.get("https://api.openweathermap.org/data/2.5/air_pollution", params=data)
        result = result.json()
    except Exception as e:
        return utils.ResultDTO(500, f"Internal Server Error: {e}").to_response()

    try:
        weather_info = result['list'][0]['components']
    except:
        return utils.ResultDTO(502, "Invalid API Response").to_response()

    return utils.ResultDTO(200, "OK", data=weather_info).to_response()