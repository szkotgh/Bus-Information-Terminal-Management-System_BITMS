import db
import modules.utils as utils

def create_audio_file(uploader_sid: int, file_name: str, file_description: str, file_org_name: str, file_path: str, file_size: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO audio_files (uploader_sid, file_name, file_description, file_org_name, file_path, file_size) VALUES (?, ?, ?, ?, ?, ?)", (uploader_sid, file_name, file_description, file_org_name, file_path, file_size))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def delete_audio_file(id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM audio_files WHERE id = ?", (id,))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="삭제되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def get_audio_file_by_id(id: int) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audio_files WHERE id = ?", (id,))
        result = cursor.fetchone()
        db.close_db_connection(conn)
        if not result:
            return db.DBResultDTO(success=False, message="올바르지 않은 ID입니다.")
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=result)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
    
def get_audio_file_list() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audio_files ORDER BY created_at DESC")
        result = cursor.fetchall()
        db.close_db_connection(conn)
        if not result:
            return db.DBResultDTO(success=False, message="파일이 존재하지 않습니다.")
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=result)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def update_audio_file(id: int, file_name: str, file_description: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE audio_files SET file_name = ?, file_description = ? WHERE id = ?", (file_name, file_description, id))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message="성공적으로 수정되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))