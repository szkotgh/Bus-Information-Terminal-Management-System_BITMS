from flask import Flask, send_file
from dotenv import load_dotenv
import os
import flask_wtf.csrf as wtf_csrf
from modules.extensions import socketio, csrf
import modules.utils as utils
import router
import sockets  # noqa: F401

load_dotenv()

app = Flask(__name__)
csrf.init_app(app)

app.secret_key = os.environ['SECRET_KEY']
app.config['SESSION_COOKIE_NAME'] = 'sid'
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_MAX_AGE'] = 3600
app.config['SESSION_COOKIE_SECURE'] = True

app.register_blueprint(router.bp)


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file('static/favicon.ico')


@app.route('/robots.txt', methods=['GET'])
def robots():
    return send_file('static/robots.txt')


@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    # response.headers['Content-Security-Policy'] = (
    #     "default-src 'self';"
    #     "script-src 'self';"
    #     "style-src 'self';"
    #     "img-src 'self' data:;"
    #     "font-src 'self';"
    #     "object-src 'none';"
    #     "base-uri 'self';"
    #     "form-action 'self';"
    # )
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    return response


@app.errorhandler(wtf_csrf.CSRFError)
def handle_csrf_error(e):
    return utils.ResultDTO(400, e).to_response()

# @app.errorhandler(Exception)
# def handle_exception(e):
#     if hasattr(e, 'code'):
#         return utils.ResultDTO(e.code, str(e)).to_response()
#     return utils.ResultDTO(500, str(e)).to_response()


if __name__ == '__main__':
    socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app, host=os.environ["HOST_IP"], port=int(
        os.environ["HOST_PORT"]), debug=True, allow_unsafe_werkzeug=True)
