import sqlite3

class DBResultDTO:
    def __init__(self, success: bool, message: str = "", data = None):
        self.success = success
        self.message = message
        self.data = data

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def close_db_connection(conn: sqlite3.Connection) -> None:
    if conn:
        conn.close()
        
def init_db():
    conn = get_db_connection()
    with open('db/schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    close_db_connection(conn)

init_db()