from flask import Blueprint, render_template, request, g, send_file
from middleware.auth import login_required
import db.domain.terminal as db_terminal
import modules.utils as utils
import modules.constants as constants
import os
from werkzeug.utils import secure_filename
import db.domain.audio_file as db_audio_file
from modules.extensions import csrf
from dotenv import load_dotenv

load_dotenv()

AUDIO_FILE_UPLOAD_PATH = os.path.abspath(os.path.join('db', 'audio_files'))
MAX_AUDIO_FILE_UPLOAD_SIZE = int(os.environ['MAX_AUDIO_FILE_UPLOAD_SIZE'])
MAX_AUDIO_FOLDER_SIZE = int(os.environ['MAX_AUDIO_FOLDER_SIZE'])

bp = Blueprint('audio_files', __name__, url_prefix='/audio')
file_bp = Blueprint('files', __name__, url_prefix='/files')
bp.register_blueprint(file_bp)

csrf.exempt(file_bp)


def get_total_folder_size():
    if not os.path.exists(AUDIO_FILE_UPLOAD_PATH):
        return 0

    total_size = 0
    try:
        for file in os.listdir(AUDIO_FILE_UPLOAD_PATH):
            file_path = os.path.join(AUDIO_FILE_UPLOAD_PATH, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    except Exception:
        return 0

    return total_size


@bp.route('', methods=['GET'])
@login_required
def index():
    terminal_list_result = db_terminal.get_terminal_list()
    max_upload_size = MAX_AUDIO_FILE_UPLOAD_SIZE
    max_folder_size = MAX_AUDIO_FOLDER_SIZE
    total_folder_size = get_total_folder_size()
    audio_file_list_result = db_audio_file.get_audio_file_list()
    host_domain = os.environ['HOST_DOMAIN']

    return render_template('manage/terminal/audio_files.html', terminal_list=terminal_list_result, max_upload_size=max_upload_size, max_folder_size=max_folder_size, total_folder_size=total_folder_size, audio_file_list=audio_file_list_result.data, host_domain=host_domain)


@bp.route('', methods=['POST'])
@login_required
def upload():
    try:
        file_name = request.form['file_name']
        file_description = request.form['file_description']
        file = request.files['file']

        file_name = file_name
        file_org_name = file.filename
        file_data = file.stream.read()
        file_size = len(file_data)

        if not file_name or not file_description or not file:
            return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()
    except Exception as e:
        return utils.ResultDTO(code=400, message=str(e)).to_response()

    # check file
    if not utils.extract_file_extension(file_org_name) in constants.AUDIO_FILE_ALLOWED_EXTENSIONS:
        return utils.ResultDTO(code=400, message=f'지원하지 않는 파일 포맷입니다. 지원 파일 포맷: {", ".join(constants.AUDIO_FILE_ALLOWED_EXTENSIONS)}').to_response()
    if file_size > MAX_AUDIO_FILE_UPLOAD_SIZE:
        return utils.ResultDTO(code=400, message=f'최대 업로드 크기를 초과했습니다. 최대 업로드 크기: {utils.format_file_size(MAX_AUDIO_FILE_UPLOAD_SIZE)}').to_response()

    # check folder size
    current_folder_size = get_total_folder_size()
    if current_folder_size + file_size > MAX_AUDIO_FOLDER_SIZE:
        return utils.ResultDTO(code=400, message=f'최대 폴더 크기를 초과했습니다. 현재 폴더 크기: {utils.format_file_size(current_folder_size)}, 최대 폴더 크기: {utils.format_file_size(MAX_AUDIO_FOLDER_SIZE)}').to_response()

    uploader_sid = g.session.data['id']
    file_path = f"{utils.generate_uuid()}.{utils.extract_file_extension(file_org_name)}"

    # file save
    try:
        os.makedirs(AUDIO_FILE_UPLOAD_PATH, exist_ok=True)
        with open(os.path.join(AUDIO_FILE_UPLOAD_PATH, file_path), 'wb') as f:
            f.write(file_data)
    except Exception as e:
        return utils.ResultDTO(code=400, message=f'파일 저장 중 오류 발생: {str(e)}').to_response()

    # audio file create
    try:
        db_audio_file.create_audio_file(
            uploader_sid, file_name, file_description, file_org_name, file_path, file_size)
    except Exception as e:
        return utils.ResultDTO(code=400, message=f'정보 저장 중 오류 발생: {str(e)}').to_response()

    return utils.ResultDTO(code=201, message="성공적으로 생성되었습니다.").to_response()


@bp.route('', methods=['DELETE'])
@login_required
def delete():
    id = request.json.get('id')
    if not id:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    audio_file_result = db_audio_file.get_audio_file_by_id(id)
    if not audio_file_result.success:
        return utils.ResultDTO(code=400, message=f"삭제에 실패했습니다: {audio_file_result.message}").to_response()

    # file remove
    try:
        if not os.path.exists(os.path.join(AUDIO_FILE_UPLOAD_PATH, audio_file_result.data['file_path'])):
            return utils.ResultDTO(code=400, message=f"파일을 찾을 수 없습니다.").to_response()

        os.remove(os.path.join(AUDIO_FILE_UPLOAD_PATH,
                  audio_file_result.data['file_path']))
    except Exception as e:
        return utils.ResultDTO(code=400, message=f"파일 삭제 중 오류 발생: {str(e)}").to_response()

    # audio file delete
    delete_result = db_audio_file.delete_audio_file(
        audio_file_result.data['id'])
    if not delete_result.success:
        return utils.ResultDTO(code=400, message=f"삭제에 실패했습니다: {delete_result.message}").to_response()

    return utils.ResultDTO(code=200, message="성공적으로 삭제되었습니다.").to_response()


@bp.route('', methods=['PUT'])
@login_required
def update():
    id = request.json.get('id')
    file_name = request.json.get('file_name')
    file_description = request.json.get('file_description')

    if not id or not file_name or not file_description:
        return utils.ResultDTO(code=400, message='누락된 값을 확인하십시오.').to_response()

    audio_file_result = db_audio_file.get_audio_file_by_id(id)
    if not audio_file_result.success:
        return utils.ResultDTO(code=400, message=f"수정에 실패했습니다: {audio_file_result.message}").to_response()

    update_result = db_audio_file.update_audio_file(
        id, file_name, file_description)
    if not update_result.success:
        return utils.ResultDTO(code=400, message=f"수정에 실패했습니다: {update_result.message}").to_response()
    return utils.ResultDTO(code=200, message=update_result.message).to_response()


@file_bp.route('/<file_path>', methods=['GET'])
def download(file_path):
    # Path Traversal check
    requested_path = os.path.join(AUDIO_FILE_UPLOAD_PATH, file_path)
    resolved_path = os.path.abspath(requested_path)
    allowed_path = os.path.abspath(AUDIO_FILE_UPLOAD_PATH)

    # Path is allowed check
    if not resolved_path.startswith(allowed_path + os.sep) and resolved_path != allowed_path:
        return utils.ResultDTO(code=403, message='접근 권한이 없습니다.').to_response()

    # File is exists check
    if not os.path.exists(resolved_path) or not os.path.isfile(resolved_path):
        return utils.ResultDTO(code=404, message='파일을 찾을 수 없습니다.').to_response()

    # File extension check
    file_extension = utils.extract_file_extension(
        os.path.basename(resolved_path))
    if file_extension.lower() not in constants.AUDIO_FILE_ALLOWED_EXTENSIONS:
        return utils.ResultDTO(code=403, message=f'지원하지 않는 파일 포맷입니다. 지원 파일 포맷: {", ".join(constants.AUDIO_FILE_ALLOWED_EXTENSIONS)}').to_response()

    # Success
    try:
        return send_file(resolved_path, as_attachment=True)
    except Exception as e:
        return utils.ResultDTO(code=400, message=f'전송 중 오류가 발생했습니다: {str(e)}').to_response()
