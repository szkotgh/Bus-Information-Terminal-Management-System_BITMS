from flask import Flask
from flask_wtf.csrf import CSRFProtect
import router
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect(app)

app.secret_key = os.environ['SECRET_KEY']
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['SESSION_COOKIE_MAX_AGE'] = 3600
app.config['SESSION_COOKIE_SECURE'] = True

app.register_blueprint(router.bp)

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

if __name__ == '__main__':
    app.run(host=os.environ["HOST_IP"], port=int(os.environ["HOST_PORT"]), debug=True)