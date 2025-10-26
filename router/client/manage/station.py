from flask import Blueprint, render_template, request
import db.domain.station as db_station
from middleware.auth import login_required
from modules import BusAPI
import modules.utils as utils

bp = Blueprint('station', __name__, url_prefix='/station')

@bp.route('', methods=['GET'])
@login_required
def index():
    station_list_result = db_station.get_station_list()
    return render_template('manage/api/station.html', station_list=station_list_result)

@bp.route('', methods=['POST'])
@login_required
def create():
    station_id = request.json.get('station_id')
    print(station_id)
    station_name = request.json.get('station_name')
    mobile_no = request.json.get('mobile_no')
    region_name = request.json.get('region_name')
    x = request.json.get('x')
    y = request.json.get('y')

    api_result = db_station.create_station(station_id, station_name, mobile_no, region_name, x, y)
    if not api_result.success:
        return utils.ResultDTO(400, f"생성에 실패했습니다: {api_result.message}").to_response()

    return utils.ResultDTO(201, api_result.message).to_response()

@bp.route('', methods=['DELETE'])
@login_required
def delete():
    station_id = request.json.get('station_id')
    api_result = db_station.delete_station(station_id)
    if not api_result.success:
        return utils.ResultDTO(400, f"삭제에 실패했습니다: {api_result.message}").to_response()

    return utils.ResultDTO(200, api_result.message).to_response()

@bp.route('', methods=['PUT'])
@login_required
def update():
    station_id = request.json.get('station_id')
    station_name = request.json.get('station_name')
    mobile_no = request.json.get('mobile_no')
    region_name = request.json.get('region_name')
    x = request.json.get('x')
    y = request.json.get('y')

    if not station_id or not station_name or not mobile_no or not region_name or x is None or y is None:
        return utils.ResultDTO(400, '누락된 값을 확인하십시오.').to_response()

    api_result = db_station.update_station(station_id, station_name, mobile_no, region_name, x, y)
    if not api_result.success:
        return utils.ResultDTO(400, f"수정에 실패했습니다: {api_result.message}").to_response()

    return utils.ResultDTO(200, api_result.message).to_response()

@bp.route('/search', methods=['GET'])
@login_required
def search_bus_station():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return utils.ResultDTO(400, '누락된 값을 확인하십시오.').to_response()

    api_result = BusAPI.search_bus_station(keyword)
    if not api_result.success:
        return utils.ResultDTO(400, f"조회에 실패했습니다: {api_result.message}").to_response()

    return utils.ResultDTO(200, api_result.message, api_result.data).to_response()