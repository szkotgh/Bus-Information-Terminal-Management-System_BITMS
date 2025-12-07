from datetime import timedelta
from flask import Blueprint, g, request
from middleware.auth import terminal_auth_token_required
from modules.extensions import csrf
import modules.utils as utils
import requests

from router.client.manage import everline

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
STATION_CODE_TO_KOREAN = {
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

# Station Code List
STATION_CODE_UPWARD = ["Y124", "Y123", "Y122", "Y121", "Y120", "Y119", "Y118",
                       "Y117", "Y116", "Y115", "Y114", "Y113", "Y112", "Y111", "Y110"]  # 상행선 역 코드
STATION_CODE_DOWNWARD = ["Y110", "Y111", "Y112", "Y113", "Y114", "Y115", "Y116",
                         "Y117", "Y118", "Y119", "Y120", "Y121", "Y122", "Y123", "Y124"]  # 하행선 역 코드

# updownCode
TRAIN_UPWARD = 1  # 상행
TRAIN_DOWNWARD = 2  # 하행

# Station Duration List
STATION_DURATION_UP = [179, 82, 77, 86, 122,
                       172, 79, 75, 62, 70, 76, 124, 85, 184, 0]
STATION_DURATION_DOWN = [89, 74, 78, 83, 121,
                         147, 79, 77, 64, 71, 102, 110, 77, 179, 0]

# Status Code
TRAIN_RETURN = 1  # 열차 회송
TRAIN_STOP = 2  # 열차 정차
TRAIN_START = 3  # 열차 출발

# Train Intervals
TRAIN_SCHEDULES = {
    "Weekday": [
        {"start": 0,    "end": 529,  "interval": -1},
        {"start": 530,  "end": 659,  "interval": 10},
        {"start": 700,  "end": 859,  "interval": 3},
        {"start": 900,  "end": 1659, "interval": 6},
        {"start": 1700, "end": 1959, "interval": 4},
        {"start": 2000, "end": 2059, "interval": 6},
        {"start": 2100, "end": 2159, "interval": 6},
        {"start": 2200, "end": 2359, "interval": 10},
    ],
    "Weekend": [
        {"start": 0,    "end": 529,  "interval": -1},
        {"start": 530,  "end": 659,  "interval": 10},
        {"start": 700,  "end": 2059, "interval": 6},
        {"start": 2100, "end": 2359, "interval": 10},
    ],
}


def get_train_schedule() -> int:
    now_datetime = utils.get_current_datetime()
    now_weekday = now_datetime.weekday()
    now_time = int(f"{now_datetime.hour:02d}{now_datetime.minute:02d}")

    # 주중
    if now_weekday in [0, 1, 2, 3, 4]:
        for schedule in TRAIN_SCHEDULES['Weekday']:
            if schedule['start'] <= now_time <= schedule['end']:
                return schedule['interval']

    # 주말
    for schedule in TRAIN_SCHEDULES['Weekend']:
        if schedule['start'] <= now_time <= schedule['end']:
            return schedule['interval']


class EverTrain:
    def __init__(self, DestCode: str, LineNo: str, StCode: str, StatusCode: str, TrainNo: str, code: str, etc: str, time: str, updownCode: str, zero: str):
        self.st_code = str(StCode)          # 현재 역 코드
        self.dest_code = str(DestCode)      # 목적지 역 코드
        self.time = int(time)               # 마지막 이벤트 후 경과 시간 (역 출발, 도착 등)
        self.updown_code = int(updownCode)  # 상행/하행 코드 (1: 상행, 2: 하행)
        self.status_code = int(StatusCode)  # 열차 상태 코드 (1: 열차 회송, 2: 열차 정차, 3: 열차 출발)
        self.train_no = int(TrainNo)        # 열차 번호
        self.line_no = str(LineNo)          # 노선 코드 (에버라인: E1)
        # self.code = int(code)               # Unknown
        # self.etc = int(etc)                 # Unknown
        # self.zero = int(zero)               # Unknown

        # ? Custom Properties
        self.next_station_code = self._get_next_station()
        self.train_schedule = get_train_schedule()

        self.time_arrival_remain = STATION_DURATION_UP[STATION_CODE_UPWARD.index(
            self.st_code)] if self.updown_code == TRAIN_UPWARD else STATION_DURATION_DOWN[STATION_CODE_DOWNWARD.index(self.st_code)]

        # to Korean
        self.st_code_korean = STATION_CODE_TO_KOREAN.get(self.st_code, None)
        self.dest_code_korean = STATION_CODE_TO_KOREAN.get(
            self.dest_code, None)
        self.updown_code_korean = "상행" if self.updown_code == TRAIN_UPWARD else "하행"
        self.status_code_korean = "회송" if self.status_code == TRAIN_RETURN else "정차" if self.status_code == TRAIN_STOP else "출발"
        self.next_station_code_korean = STATION_CODE_TO_KOREAN.get(
            self.next_station_code, None)

    def _get_next_station(self) -> str:
        if self.updown_code == TRAIN_UPWARD:
            if self.st_code == STATION_CODE_UPWARD[-1]:
                return STATION_CODE_UPWARD[-2]
            else:
                return STATION_CODE_UPWARD[STATION_CODE_UPWARD.index(self.st_code) + 1]
        else:
            if self.st_code == STATION_CODE_DOWNWARD[-1]:
                return STATION_CODE_DOWNWARD[-2]
            else:
                return STATION_CODE_DOWNWARD[STATION_CODE_DOWNWARD.index(self.st_code) + 1]

    def to_dict(self):
        return self.__dict__


cache_time = None
cache_return_data = None


@bp.route('', methods=['GET'])
# @terminal_auth_token_required
def index():
    global cache_time, cache_return_data
    if cache_time and cache_time + timedelta(seconds=1) > utils.get_current_datetime():
        return utils.ResultDTO(200, "OK(Cache)", data=cache_return_data).to_response()

    cache_time = utils.get_current_datetime()

    # Get data
    try:
        result = requests.get("https://everlinecu.com/api/api009.json")
        result = result.json()
        if result.get('code', None) != 200:
            raise Exception(result.get(
                'msg', 'No message, Invalid Response Code'))
    except Exception as e:
        return utils.ResultDTO(500, f"Eveline Server Error: {e}").to_response()

    # Data Processing
    everline_object_list: list[EverTrain] = []
    try:
        for item in result['data']:
            # if item['TrainNo'] != "3":
            #     continue
            everline_object_list.append(EverTrain(
                DestCode=item['DestCode'],
                LineNo=item['LineNo'],
                StCode=item['StCode'],
                StatusCode=item['StatusCode'],
                TrainNo=item['TrainNo'],
                code=item['code'],
                etc=item['etc'],
                time=item['time'],
                updownCode=item['updownCode'],
                zero=item['zero'],
            ))
    except Exception as e:
        return utils.ResultDTO(500, f"Data Parsing Error: {e}").to_response()

    # Return
    return_data = {
        "train_schedule": get_train_schedule(),
        "train_list": list()
    }
    for everline_object in everline_object_list:
        return_data['train_list'].append(everline_object.to_dict())

    cache_return_data = return_data

    return utils.ResultDTO(200, "OK", data=return_data).to_response()
