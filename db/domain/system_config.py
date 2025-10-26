import sqlite3
import db.__init__ as db

def get_config_by_key(config_key: str) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system_config WHERE config_key = ?", (config_key,))
        result = cursor.fetchone()
        db.close_db_connection(conn)
        
        if not result:
            return db.DBResultDTO(success=False, message=f"잘못된 키입니다.")
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=result)
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def create_kv(config_key: str, config_value: str, description: str = None) -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO system_config (config_key, config_value, description) VALUES (?, ?, ?)", (config_key, config_value, description))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message=f"성공적으로 생성되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def update_kv(config_key: str, config_value: str, description: str = None) -> db.DBResultDTO:
    config_result = get_config_by_key(config_key)
    if not config_result.success:
        return config_result
    
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE system_config SET config_value = ?, description = ?, updated_at = CURRENT_TIMESTAMP WHERE config_key = ?", (config_value, description, config_key))
        conn.commit()
        db.close_db_connection(conn)
        return db.DBResultDTO(success=True, message=f"성공적으로 저장되었습니다.")
    except Exception as e:
        return db.DBResultDTO(success=False, message=f"{str(e)}")

def get_all_configs() -> db.DBResultDTO:
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT config_key, config_value, description, created_at, updated_at FROM system_config ORDER BY config_key")
        results = cursor.fetchall()
        
        conn.close()
        
        configs = []
        for result in results:
            configs.append({
                'config_key': result[0],
                'config_value': result[1],
                'description': result[2],
                'created_at': result[3],
                'updated_at': result[4]
            })
        
        return db.DBResultDTO(success=True, message="성공적으로 조회되었습니다.", data=configs)
        
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))

def delete_config(config_key: str) -> db.DBResultDTO:
    config_result = get_config_by_key(config_key)
    if not config_result.success:
        return config_result
    
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM system_config WHERE config_key = ?", (config_key,))
        conn.commit()
        db.close_db_connection(conn)
        
        return db.DBResultDTO(success=True, message=f"성공적으로 삭제되었습니다.")
        
    except Exception as e:
        return db.DBResultDTO(success=False, message=str(e))
