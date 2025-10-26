import db
import modules.utils as utils
import modules.constants as constants

def create_session(ip: str, user_agent: str, checksum: str) -> db.DBResultDTO:
    session_id = utils.generate_uuid()
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_session (session_id, ip, user_agent, checksum) VALUES (?, ?, ?, ?)", (session_id, ip, user_agent, checksum))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 생성되었습니다.", data=session_id)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_session_by_session_id(session_id: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_session WHERE session_id = ?", (session_id,))
        session = cursor.fetchone()
        db.close_db_connection(conn)
        if not session:
            return db.DBResultDTO(success=False, message="올바르지 않은 ID입니다.")
        return db.DBResultDTO(success=True, message="조회되었습니다.", data=session)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_session_by_id(id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_session WHERE id = ?", (id,))
        session = cursor.fetchone()
        db.close_db_connection(conn)
        if not session:
            return db.DBResultDTO(success=False, message="올바르지 않은 ID입니다.")
        return db.DBResultDTO(success=True, message="조회되었습니다.", data=session)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_session_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_session ORDER BY created_at DESC")
        sessions = cursor.fetchall()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="조회되었습니다.", data=sessions)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def deactivate_session_by_session_id(session_id: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE login_session SET status = ? WHERE session_id = ?", (constants.STATUS_INACTIVE, session_id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="비활성화했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def block_session_by_session_id(session_id: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE login_session SET status = ? WHERE session_id = ?", (constants.STATUS_BLOCKED, session_id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="블로킹했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def deactivate_session_by_id(id: int) -> db.DBResultDTO:
    session_result = get_session_by_id(id)
    if not session_result.success:
        return session_result
    
    if not session_result.data['status'] == constants.STATUS_ACTIVE:
        return db.DBResultDTO(success=False, message="비활성화할 수 있는 상태가 아닙니다.")

    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE login_session SET status = ? WHERE id = ?", (constants.STATUS_INACTIVE, session_result.data['id']))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="비활성화했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def deactivate_all_sessions() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE login_session SET status = ? WHERE status = ?", (constants.STATUS_INACTIVE, constants.STATUS_ACTIVE))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="모든 세션을 비활성화했습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))