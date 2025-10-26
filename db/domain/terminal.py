import db
import modules.utils as utils
import modules.constants as constants

class TerminalDTO:
    def __init__(self, id: int, name: str, auth_token: str, status: str, created_at: str):
        self.id = id
        self.name = name
        self.auth_token = auth_token
        self.status = status
        self.created_at = created_at

def create_terminal(terminal_name: str, terminal_auth_token: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO terminal (name, auth_token) VALUES (?, ?)", (terminal_name, terminal_auth_token))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_terminal_by_id(terminal_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminal WHERE id = ?", (terminal_id,))
        terminal = cursor.fetchone()
        db.close_db_connection(conn)
        if terminal:
            return db.DBResultDTO(success=True, message="성공적으로 조회했습니다.", data=terminal)
        else:
            return db.DBResultDTO(success=False, message="올바르지 않은 단말기 ID입니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_terminal_by_auth_token(auth_token: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminal WHERE auth_token = ?", (auth_token,))
        terminal = cursor.fetchone()
        db.close_db_connection(conn)
        if not terminal:
            return db.DBResultDTO(success=False, message="invalid auth token.")
        return db.DBResultDTO(success=True, message="success", data=terminal)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_terminal_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminal")
        terminals = cursor.fetchall()
        db.close_db_connection(conn)
        if not terminals:
            return db.DBResultDTO(success=False, message="터미널이 없습니다.")
        
        return db.DBResultDTO(success=True, message="성공적으로 조회했습니다.", data=terminals)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def delete_terminal(terminal_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM terminal WHERE id = ?", (terminal_id,))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def update_terminal(terminal_id: int, terminal_name: str, terminal_status: str) -> db.DBResultDTO:
    if terminal_status not in constants.TERMINAL_STATUS_LIST:
        return utils.ResultDTO(code=400, message='유효하지 않은 상태입니다.')
    
    terminal_result = get_terminal_by_id(terminal_id)
    if not terminal_result.success:
        return terminal_result
    
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE terminal SET name = ?, status = ? WHERE id = ?", (terminal_name, terminal_status, terminal_result.data['id']))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="업데이트 되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def update_terminal_auth_token(terminal_id: int) -> db.DBResultDTO:
    terminal_result = get_terminal_by_id(terminal_id)
    if not terminal_result.success:
        return terminal_result
    
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE terminal SET auth_token = ? WHERE id = ?", (utils.generate_hash(16), terminal_result.data['id']))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="갱신되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))