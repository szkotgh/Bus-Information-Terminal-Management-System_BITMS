from flask import request, g
from flask_socketio import emit, join_room, leave_room, rooms
from modules.extensions import socketio
from middleware.auth import socket_token_or_login_required, login_required
import binascii
import base64


sid_to_terminal = {}


@socketio.on('connect', namespace='/terminal')
@socket_token_or_login_required
def handle_socket_connect():
    terminal = g.get('terminal')
    
    if terminal:
        sid_to_terminal[request.sid] = terminal

@socketio.on('disconnect', namespace='/terminal')
@socket_token_or_login_required
def handle_socket_disconnect():
    if request.sid in sid_to_terminal:
        try:
            del sid_to_terminal[request.sid]
        except Exception:
            pass

@socketio.on('join_terminal', namespace='/terminal')
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
    join_room(f"terminal:{terminal_id_int}", sid=sid)
    emit('info', {'message': f'joined terminal:{terminal_id_int}'}, room=sid)

@socketio.on('leave_terminal', namespace='/terminal')
@login_required
def handle_leave_terminal(terminal_id=None):
    sid = request.sid
    try:
        target_room = f"terminal:{int(terminal_id)}" if terminal_id is not None else None
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

    

@socketio.on('status', namespace='/terminal')
@socket_token_or_login_required
def handle_socket_status(status):
    terminal = sid_to_terminal.get(request.sid) or g.get('terminal')
    if terminal:
        room = f"terminal:{terminal['id']}"
        socketio.emit('device_status', status, room=room, namespace='/terminal')

@socketio.on('command', namespace='/terminal')
@login_required
def handle_socket_command(data):
    command = data.get('command')
    terminal_id = data.get('terminal_id')
    
    if not command or not terminal_id:
        emit('error', {'message': 'invalid command data'}, room=request.sid)
        return
    
    for terminal in sid_to_terminal:
        if sid_to_terminal[terminal]['id'] == terminal_id:
            socketio.emit('command', command, to=terminal, namespace='/terminal')
            return