from flask import request, g
from flask_socketio import emit, join_room, leave_room, rooms
from modules.extensions import socketio
from middleware.auth import login_required, socket_token_required, socket_token_or_login_required
import binascii
import base64


sid_to_terminal = {}


def _room_name(terminal_id: int) -> str:
    return f"terminal:{terminal_id}"


@socketio.on('connect', namespace='/terminal/livescreen')
@socket_token_or_login_required
def handle_socket_connect():
    terminal = g.get('terminal')
    
    if terminal:
        sid_to_terminal[request.sid] = terminal

@socketio.on('disconnect', namespace='/terminal/livescreen')
@socket_token_or_login_required
def handle_socket_disconnect():
    if request.sid in sid_to_terminal:
        try:
            del sid_to_terminal[request.sid]
        except Exception:
            pass


@socketio.on('join_terminal', namespace='/terminal/livescreen')
@login_required
def handle_join_terminal(terminal_id):
    sid = request.sid
    try:
        terminal_id_int = int(terminal_id)
    except Exception:
        emit('error', {'message': 'invalid terminal id'}, room=sid)
        return

    try:
        current_rooms = rooms(sid)
        for r in current_rooms:
            if isinstance(r, str) and r.startswith('terminal:'):
                leave_room(r, sid=sid)
    except Exception:
        pass
    join_room(_room_name(terminal_id_int), sid=sid)
    emit('info', {'message': f'joined {_room_name(terminal_id_int)}'}, room=sid)


@socketio.on('leave_terminal', namespace='/terminal/livescreen')
@login_required
def handle_leave_terminal(terminal_id=None):
    sid = request.sid
    try:
        target_room = _room_name(int(terminal_id)) if terminal_id is not None else None
    except Exception:
        target_room = None

    try:
        current_rooms = rooms(sid)
        for r in current_rooms:
            if isinstance(r, str) and r.startswith('terminal:'):
                if target_room is None or r == target_room:
                    leave_room(r, sid=sid)
    except Exception:
        pass
    emit('info', {'message': 'left terminal rooms'}, room=sid)


@socketio.on('frame', namespace='/terminal/livescreen')
@socket_token_or_login_required
def handle_frame(data):
    sid = request.sid
    terminal = sid_to_terminal.get(sid) or g.get('terminal')
    if not terminal:
        emit('error', {'message': 'terminal unauthorized'}, room=sid)
        return

    screen_hex = data.get('screen')
    if not screen_hex or not isinstance(screen_hex, str):
        emit('error', {'message': 'invalid screen payload'}, room=sid)
        return

    try:
        webp_bytes = binascii.unhexlify(screen_hex.strip())
    except (binascii.Error, ValueError):
        emit('error', {'message': 'invalid hex format'}, room=sid)
        return

    base64_data = base64.b64encode(webp_bytes).decode('ascii')
    room = _room_name(int(terminal['id']))
    socketio.emit('livescreen', base64_data, room=room, namespace='/terminal/livescreen')


