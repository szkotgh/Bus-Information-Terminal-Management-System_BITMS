import db
import modules.utils as utils
import modules.constants as constants

def create_station(station_id: int, station_name: str, mobile_no: int, region_name: str, x: float, y: float) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO station (station_id, station_name, mobile_no, region_name, x, y) VALUES (?, ?, ?, ?, ?, ?)", (station_id, station_name, mobile_no, region_name, x, y))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 등록되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def get_station_by_id(station_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM station WHERE station_id = ?", (station_id,))
        station = cursor.fetchone()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 조회했습니다.", data=station)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_station_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM station")
        stations = cursor.fetchall()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 조회했습니다.", data=stations)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def delete_station(station_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM station WHERE station_id = ?", (station_id,))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def update_station(station_id: int, station_name: str, mobile_no: int, region_name: str, x: float, y: float) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE station SET station_name = ?, mobile_no = ?, region_name = ?, x = ?, y = ? WHERE station_id = ?", (station_name, mobile_no, region_name, x, y, station_id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 수정되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))