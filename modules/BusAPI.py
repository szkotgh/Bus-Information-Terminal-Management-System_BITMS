import requests
import os

class StationDTO:
    def __init__(self, station_id: int, station_name: str, mobile_no: int, region_name: str, x: float, y: float, created_at: str):
        self.station_id = station_id
        self.station_name = station_name
        self.mobile_no = mobile_no
        self.region_name = region_name
        self.x = x
        self.y = y
        self.created_at = created_at

class StationBusViaRoutesDTO:
    def __init__(
        self, id: int, station_id: int, route_id: int, route_name: str, route_type_cd: int,
        region_name: str, route_dest_id: int, route_dest_name: str, route_type_name: str,
        sta_order: int, created_at: str
    ):
        self.id = id
        self.station_id = station_id
        self.route_id = route_id
        self.route_name = route_name
        self.route_type_cd = route_type_cd
        self.region_name = region_name
        self.route_dest_id = route_dest_id
        self.route_dest_name = route_dest_name
        self.route_type_name = route_type_name
        self.sta_order = sta_order
        self.created_at = created_at

class BusRouteStationListDTO:
    def __init__(
        self, route_id: int, station_seq: int, station_id: int, station_name: str,
        mobile_no: int, district_cd: int, region_name: str, x: float, y: float,
        turn_seq: int, turn_yn: str, created_at: str
    ):
        self.route_id = route_id
        self.station_seq = station_seq
        self.station_id = station_id
        self.station_name = station_name
        self.mobile_no = mobile_no
        self.district_cd = district_cd
        self.region_name = region_name
        self.x = x
        self.y = y
        self.turn_seq = turn_seq
        self.turn_yn = turn_yn
        self.created_at = created_at

class APIResultDTO:
    def __init__(self, code: int, success: bool, message: str = '', data=None):
        self.code = code
        self.success = success
        self.message = message
        self.data = data

def api_request(cmd, **kwargs) -> APIResultDTO:
    url = "https://www.gbis.go.kr/gbis2014/openAPI.action"
    params = {
        'cmd': cmd,
        'serviceKey': os.environ['DATA_GO_KR_SERVICEKEY'],
        **kwargs,
        'format': 'json',
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        print(response.url)
        result_code = response.json()['response']['msgHeader']['resultCode']
        result_code = int(result_code)
        result_message = response.json()['response']['msgHeader']['resultMessage']
        result_data = response.json()['response'].get('msgBody', None)
        return APIResultDTO(code=result_code, success=(result_code == 0), message=result_message, data=result_data)
    except Exception as e:
        return APIResultDTO(code=-1, success=False, message=str(e))

def search_bus_station(keyword: str) -> APIResultDTO:
    request_result = api_request('getBusStation', keyword=keyword)
    if not request_result.success:
        return request_result
    
    request_result.data = request_result.data.get('busStationList', [])
    if type(request_result.data) is dict:
        request_result.data = [request_result.data]
    return request_result
    
def get_station_bus_route_list(stationId: str) -> APIResultDTO:
    request_result = api_request('getBusStationRoute', stationId=stationId)
    if not request_result.success:
        return request_result
    
    request_result.data = request_result.data.get('busRouteList', [])
    if type(request_result.data) is dict:
        request_result.data = [request_result.data]
    return request_result
    
def get_bus_route_station_list(routeId: str) -> APIResultDTO:
    request_result = api_request('getBusRouteStation', routeId=routeId)
    if not request_result.success:
        return request_result
    
    request_result.data = request_result.data.get('busRouteStationList', [])
    if type(request_result.data) is dict:
        request_result.data = [request_result.data]
    return request_result
    
def get_bus_arrival_station(stationId: str) -> APIResultDTO:
    request_result = api_request('getBusArrivalStation', stationId=stationId)
    if not request_result.success:
        return request_result
    
    request_result.data = request_result.data.get('busArrivalList', [])
    if type(request_result.data) is dict:
        request_result.data = [request_result.data]
    return request_result
    
