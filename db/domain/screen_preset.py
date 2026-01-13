import db
import modules.utils as utils
import modules.constants as constants


def create_screen_preset(name: str, command: str, value1_desc: str = '', value2_desc: str = '', value3_desc: str = '', value4_desc: str = '') -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO terminal_screen_preset (name, command, value1_desc, value2_desc, value3_desc, value4_desc) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, command, value1_desc, value2_desc, value3_desc, value4_desc))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def get_screen_preset_by_id(id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM terminal_screen_preset WHERE id = ?", (id,))
        screen_preset = cursor.fetchone()
        db.close_db_connection(conn)
        if not screen_preset:
            return db.DBResultDTO(success=False, message="올바르지 않은 프리셋 ID입니다.")
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=screen_preset)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def get_screen_preset_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminal_screen_preset")
        screen_preset_list = cursor.fetchall()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=screen_preset_list)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def delete_screen_preset(id: int) -> db.DBResultDTO:
    screen_preset_result = get_screen_preset_by_id(id)
    if not screen_preset_result.success:
        return screen_preset_result

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM terminal_screen_preset WHERE id = ?", (id,))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def update_screen_preset(id: int, name: str, command: str, value1_desc: str = '', value2_desc: str = '', value3_desc: str = '', value4_desc: str = '') -> db.DBResultDTO:
    screen_preset_result = get_screen_preset_by_id(id)
    if not screen_preset_result.success:
        return screen_preset_result

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE terminal_screen_preset SET name = ?, command = ?, value1_desc = ?, value2_desc = ?, value3_desc = ?, value4_desc = ? WHERE id = ?",
                       (name, command, value1_desc, value2_desc, value3_desc, value4_desc, id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 업데이트되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
