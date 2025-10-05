import db
import modules.utils as utils

def create_terminal(terminal_name: str, terminal_auth_token: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO terminals (name, auth_token) VALUES (?, ?)", (terminal_name, terminal_auth_token))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_terminal_by_id(terminal_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminals WHERE id = ?", (terminal_id,))
        terminal = cursor.fetchone()
        db.close_db_connection(conn)
        if terminal:
            return db.DBResultDTO(success=True, message="성공적으로 조회했습니다.", data=terminal)
        else:
            return db.DBResultDTO(success=False, message="올바르지 않은 ID입니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def get_terminal_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terminals ORDER BY id DESC")
        terminals = cursor.fetchall()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 조회했습니다.", data=terminals)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def delete_terminal(terminal_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM terminals WHERE id = ?", (terminal_id,))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def update_terminal(terminal_id: int, terminal_name: str, terminal_status: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE terminals SET name = ?, status = ? WHERE id = ?", (terminal_name, terminal_status, terminal_id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="업데이트 되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def update_terminal_auth_token(terminal_id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE terminals SET auth_token = ? WHERE id = ?", (utils.generate_hash(16), terminal_id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="갱신되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))