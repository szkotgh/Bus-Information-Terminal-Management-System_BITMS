from flask import Blueprint, g, request
from modules import BusAPI
import modules.utils as utils
from middleware.auth import terminal_auth_token_required
from modules.extensions import csrf

bp = Blueprint('bus', __name__, url_prefix='/bus')

csrf.exempt(bp)

@bp.route('', methods=['GET'])
def index():
    return utils.ResultDTO(200, "Bus API Endpoint").to_response()

@bp.route('/getBusStation', methods=['GET'])
@terminal_auth_token_required
def get_bus_station():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return utils.ResultDTO(400, '누락된 값을 확인하십시오.').to_response()

    api_result = BusAPI.search_bus_station(keyword)
    if not api_result.success:
        return utils.ResultDTO(400, api_result.message).to_response()

    return utils.ResultDTO(200, '조회 성공했습니다.', api_result.data).to_response()

@bp.route('/getBusStationRoute', methods=['GET'])
@terminal_auth_token_required
def get_bus_station_route():
    station_id = request.args.get('stationId', '')
    if not station_id:
        return utils.ResultDTO(400, '누락된 값을 확인하십시오.').to_response()

    api_result = BusAPI.get_station_bus_route_list(station_id)
    if not api_result.success:
        return utils.ResultDTO(400, api_result.message).to_response()

    return utils.ResultDTO(200, '조회 성공했습니다.', api_result.data).to_response()

@bp.route('/getBusRouteStation', methods=['GET'])
@terminal_auth_token_required
def get_bus_route_station():
    routeId = request.args.get('routeId', '')
    stationSeq = request.args.get('stationSeq', type=int, default=None)
    if not routeId:
        return utils.ResultDTO(400, '누락된 값을 확인하십시오.').to_response()
    if stationSeq != None and stationSeq <= 0:
        return utils.ResultDTO(400, '유효하지 않은 값을 확인하십시오.').to_response()

    api_result = BusAPI.get_bus_route_station_list(routeId)
    if not api_result.success:
        return utils.ResultDTO(400, api_result.message).to_response()

    if not stationSeq == None:
        if stationSeq > len(api_result.data):
            return utils.ResultDTO(400, '유효하지 않은 값을 확인하십시오.').to_response()
        stationSeqData = api_result.data[stationSeq-1]
        return utils.ResultDTO(200, '조회 성공했습니다.', stationSeqData).to_response()

    return utils.ResultDTO(200, '조회 성공했습니다.', api_result.data).to_response()

@bp.route('/busArrivalList', methods=['GET'])
@terminal_auth_token_required
def bus_arrival_list():
    stationId = request.args.get('stationId', '')
    if not stationId:
        return utils.ResultDTO(400, '누락된 값을 확인하십시오.').to_response()

    api_result = BusAPI.get_bus_arrival_station(stationId)
    if not api_result.success:
        return utils.ResultDTO(400, api_result.message).to_response()

    return utils.ResultDTO(200, '조회 성공했습니다.', api_result.data).to_response()