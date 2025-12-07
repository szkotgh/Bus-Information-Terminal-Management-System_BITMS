import os
import uuid
import hashlib
import re
from flask import request
from datetime import datetime, timedelta

class ResultDTO():
    def __init__(self, code, message, data: dict = {}, success: bool = False):
        self.code = code
        self.message = message
        self.data = data
        self.success = success

    def to_response(self):
        response = {
            "code":    int(self.code),
            "message": str(self.message),
            "data":    self.data
        }
        return response, self.code

def generate_uuid() -> str:
    return str(uuid.uuid4())

def generate_hash(len: int) -> str:
    return os.urandom(16).hex()[:len]

def str_to_hash(input_string: str) -> str:
    return hashlib.sha256(input_string.encode()).hexdigest()

def create_session_checksum(ip: str, user_agent: str) -> str:
    return str_to_hash(f"{ip}|{user_agent}")

def create_session_checksum_from_request() -> str:
    ip = get_client_ip()
    user_agent = get_user_agent()
    return create_session_checksum(ip, user_agent)

def get_client_ip():
    user_ip = request.headers.get("Cf-Connecting-Ip", request.remote_addr) # Written based on Cloudflare
    return f'{user_ip}'

def get_user_agent() -> str:
    return request.headers.get('User-Agent', 'Unknown')

def check_password(password: str, hashed_password: str, salt: str) -> bool:
    return str_to_hash(password + salt) == hashed_password

def extract_bearer_token(authorization: str) -> str:
    if not authorization: return None
    if not authorization.startswith('Bearer '): return None
    
    return authorization.split(' ')[1]

def extract_file_extension(file_name: str) -> str:
    extension = file_name.strip().lower().split('.')[-1]
    return extension

def format_file_size(file_size: int) -> str:
    size_list = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    size_index = 0
    while file_size > 1000:
        file_size /= 1000
        size_index += 1
    return f"{file_size:.2f} {size_list[size_index]}"

# Datetime
def get_current_datetime() -> datetime:
    return datetime.utcnow() + timedelta(hours=9)

def get_current_datetime_str() -> str:
    return (datetime.utcnow() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')

def str_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def datetime_to_str(date: datetime) -> str:
    return date.strftime('%Y-%m-%d %H:%M:%S')

def is_minutes_passed(start_time: str, minutes: int) -> bool:
    start_dt = str_to_datetime(start_time)
    target_time = start_dt + timedelta(minutes=minutes)
    now_time = get_current_datetime()
    print(now_time, target_time)
    return now_time > target_time

def get_future_timestamp(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime:
    future_datetime = get_current_datetime() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return future_datetime

# regex
class RegexResultDTO():
    def __init__(self, success: bool, detail: str):
        self.success = success
        self.detail = detail

def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return RegexResultDTO(success=False, detail="8자리 이상이어야 합니다.")
    if re.search(r'\s', password):
        return RegexResultDTO(success=False, detail="공백은 허용하지 않습니다.")
    if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>/?]+$', password):
        return RegexResultDTO(success=False, detail="영숫자, 기호만 사용 가능합니다.")
    return RegexResultDTO(success=True, detail="비밀번호가 유효합니다.")

