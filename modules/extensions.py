from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect

socketio: SocketIO = SocketIO(cors_allowed_origins="*")
csrf: CSRFProtect = CSRFProtect()


