import db
import db.domain.terminal as db_terminal
import db.domain.screen_preset as db_screen_preset
import modules.constants as constants


def _add_preset_info_to_screen_show(screen_show):
    screen_show_dict = dict(screen_show) if not isinstance(
        screen_show, dict) else screen_show
    preset_info_result = db_screen_preset.get_screen_preset_by_id(
        screen_show_dict['screen_preset_id'])
    if preset_info_result.success and preset_info_result.data:
        screen_show_dict['preset_info'] = dict(preset_info_result.data)
    return screen_show_dict


def create_screen_show(terminal_id: int, screen_preset_id: int, is_active: bool, order_id: int, desc: str, value1: str = '', value2: str = '', value3: str = '', value4: str = '') -> db.DBResultDTO:
    terminal_result = db_terminal.get_terminal_by_id(terminal_id)
    if not terminal_result.success:
        return terminal_result
    screen_preset_result = db_screen_preset.get_screen_preset_by_id(
        screen_preset_id)
    if not screen_preset_result.success:
        return screen_preset_result
    if is_active not in constants.SCREEN_SHOW_IS_ACTIVE_LIST:
        return db.DBResultDTO(success=False, message="활성화 상태가 올바르지 않습니다.")

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO terminal_screen_show (terminal_id, screen_preset_id, is_active, order_id, desc, value1, value2, value3, value4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (terminal_id, screen_preset_id, is_active, order_id, desc, value1, value2, value3, value4))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def get_screen_show_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminal_screen_show")
        screen_show_rows = cursor.fetchall()
        db.close_db_connection(conn)

        screen_show_list = []
        for row in screen_show_rows:
            screen_show_dict = _add_preset_info_to_screen_show(row)
            screen_show_list.append(screen_show_dict)

        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=screen_show_list)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def get_screen_show_by_id(screen_show_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM terminal_screen_show WHERE id = ?", (screen_show_id,))
        screen_show = cursor.fetchone()
        db.close_db_connection(conn)
        if not screen_show:
            return db.DBResultDTO(success=False, message="올바르지 않은 화면 ID입니다.")

        screen_show_dict = _add_preset_info_to_screen_show(screen_show)
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=screen_show_dict)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def get_screen_show_by_terminal_id(terminal_id: int) -> db.DBResultDTO:
    terminal_result = db_terminal.get_terminal_by_id(terminal_id)
    if not terminal_result.success:
        return terminal_result

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM terminal_screen_show WHERE terminal_id = ? ORDER BY order_id ASC", (terminal_id,))
        screen_show_rows = cursor.fetchall()
        if not screen_show_rows:
            return db.DBResultDTO(success=False, message="생성된 정보가 없습니다.")

        screen_show_list = []
        for row in screen_show_rows:
            screen_show_dict = _add_preset_info_to_screen_show(row)
            screen_show_list.append(screen_show_dict)

        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=screen_show_list)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def delete_screen_show(screen_show_id: int) -> db.DBResultDTO:
    screen_show_result = get_screen_show_by_id(screen_show_id)
    if not screen_show_result.success:
        return screen_show_result

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM terminal_screen_show WHERE id = ?", (screen_show_id,))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))


def update_screen_show(screen_show_id: int, terminal_id: int, screen_preset_id: int, is_active: bool, order_id: int, desc: str, value1: str = '', value2: str = '', value3: str = '', value4: str = '') -> db.DBResultDTO:
    terminal_result = db_terminal.get_terminal_by_id(terminal_id)
    if not terminal_result.success:
        return terminal_result
    screen_preset_result = db_screen_preset.get_screen_preset_by_id(
        screen_preset_id)
    if not screen_preset_result.success:
        return screen_preset_result
    if is_active not in constants.SCREEN_SHOW_IS_ACTIVE_LIST:
        return db.DBResultDTO(success=False, message="활성화 상태가 올바르지 않습니다.")

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE terminal_screen_show SET terminal_id = ?, screen_preset_id = ?, is_active = ?, order_id = ?, desc = ?, value1 = ?, value2 = ?, value3 = ?, value4 = ? WHERE id = ?",
                       (terminal_id, screen_preset_id, is_active, order_id, desc, value1, value2, value3, value4, screen_show_id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 수정되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
