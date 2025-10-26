from flask import Blueprint, g, request
from middleware.auth import terminal_auth_token_required
from modules.extensions import csrf
import modules.utils as utils
import requests

bp = Blueprint('everline', __name__, url_prefix='/everline')

csrf.exempt(bp)


# Station Name List
STATION_NAME = [
    ['기흥', 'Giheung'],
    ['강남대', 'KANGNAM UNIV.'],
    ['지석', 'JISEOK'],
    ['어정', 'EOJEONG'],
    ['동백', 'DONGBAEK'],
    ['초당', 'CHODANG'],
    ['삼가', 'SAMGA'],
    ['시청·용인대', 'Cityhall·Yongin Univ'],
    ['명지대', 'MYONGJI UNIV.'],
    ['김량장', 'GIMYANGJANG'],
    ['용인중앙시장', 'Yongin Jungang Market'],
    ['고진', 'GOJIN'],
    ['보평', 'BOPYEONG'],
    ['둔전', 'DUNJEON'],
    ['전대·에버랜드', 'JEONDAE·EVERLAND']
]

# Station Code List
STATION_CODE = {
    "Y110": "기흥",
    "Y111": "강남대",
    "Y112": "지석",
    "Y113": "어정",
    "Y114": "동백",
    "Y115": "초당",
    "Y116": "삼가",
    "Y117": "시청·용인대",
    "Y118": "명지대",
    "Y119": "김량장",
    "Y120": "용인중앙시장",
    "Y121": "고진",
    "Y122": "보평",
    "Y123": "둔전",
    "Y124": "전대·에버랜드"
}
STATION_CODE_UPWARD   = ["Y124", "Y123", "Y122", "Y121", "Y120", "Y119", "Y118", "Y117", "Y116", "Y115", "Y114", "Y113", "Y112", "Y111", "Y110"] # 상행선 역 코드
STATION_CODE_DOWNWARD = ["Y110", "Y111", "Y112", "Y113", "Y114", "Y115", "Y116", "Y117", "Y118", "Y119", "Y120", "Y121", "Y122", "Y123", "Y124"] # 하행선 역 코드

# updownCode 
TRAIN_UPWARD   = "1" # 상행
TRAIN_DOWNWARD = "2" # 하행

# Status Code
TRAIN_RETURN = "1" # 열차 회송
TRAIN_STOP   = "2" # 열차 정차
TRAIN_START  = "3" # 열차 출발

# Train Intervals
TRAIN_SCHEDULES = {
    "Weekday": [
        {"start": 0,    "end": 459,  "interval": None},
        {"start": 530,  "end": 659,  "interval": 10},
        {"start": 700,  "end": 859,  "interval": 3},
        {"start": 900,  "end": 1659, "interval": 6},
        {"start": 1700, "end": 1959, "interval": 4},
        {"start": 2000, "end": 2059, "interval": 6},
        {"start": 2100, "end": 2159, "interval": 6},
        {"start": 2200, "end": 2359, "interval": 10},
    ],
    "Weekend": [
        {"start": 0,    "end": 459,  "interval": None},
        {"start": 530,  "end": 659,  "interval": 10},
        {"start": 700,  "end": 2059, "interval": 6},
        {"start": 2100, "end": 2359, "interval": 10},
    ],
}

class EverTrain:
    def __init__(self, DestCode: str, LineNo: str, StCode: str, StatusCode: str, TrainNo: str, code: str, etc: str, time: str, updownCode: str, zero: str):
        self.DestCode = DestCode
        self.LineNo = LineNo
        self.StCode = StCode
        self.StatusCode = StatusCode
        self.TrainNo = TrainNo
        self.code = code
        self.etc = etc
        self.time = time
        self.updownCode = updownCode
        self.zero = zero

@bp.route('', methods=['GET'])
def index():
    result = requests.get("https://everlinecu.com/api/api009.json")
    result = result.json()
    
    return utils.ResultDTO(200, "OK", data=result['data']).to_response()
