CREATE TABLE IF NOT EXISTS login_session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    ip TEXT NOT NULL,
    user_agent TEXT NOT NULL,
    checksum TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours'))
);

CREATE TABLE IF NOT EXISTS terminal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    auth_token TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'active',
    manager TEXT DEFAULT '지정안됨',
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours'))
);

CREATE TABLE IF NOT EXISTS terminal_screen_preset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    command TEXT NOT NULL UNIQUE,
    value_desc TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours'))
);

CREATE TABLE IF NOT EXISTS terminal_screen_show (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    terminal_id INTEGER NOT NULL,
    screen_preset_id INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    order_id INTEGER NOT NULL,
    desc TEXT DEFAULT '',
    value TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours')),
    FOREIGN KEY (terminal_id) REFERENCES terminal(id) ON DELETE CASCADE,
    FOREIGN KEY (screen_preset_id) REFERENCES terminal_screen_preset(id) ON DELETE CASCADE
);

-- CREATE TABLE IF NOT EXISTS terminal_status (
--     terminal_id INTEGER NOT NULL,
--     ...
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     PRIMARY KEY (terminal_id),
--     FOREIGN KEY (terminal_id) REFERENCES terminal(id) ON DELETE CASCADE
-- );

CREATE TABLE IF NOT EXISTS station (
    station_id INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL,
    mobile_no INTEGER NOT NULL,
    region_name TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours'))
);

CREATE TABLE IF NOT EXISTS audio_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uploader_sid INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_description TEXT,
    file_org_name TEXT NOT NULL,
    file_path TEXT UNIQUE NOT NULL,
    file_size INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours')),
    FOREIGN KEY (uploader_sid) REFERENCES login_session(id)
);

CREATE TABLE IF NOT EXISTS system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key TEXT UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT (datetime('now', '+9 hours')),
    created_at TIMESTAMP DEFAULT (datetime('now', '+9 hours'))
);
