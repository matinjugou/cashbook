from utils import *
from views.cashbook import cashbook
import settings

from flask import Flask, make_response, request
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(cashbook, url_prefix='/api/book')
app.debug = settings.debug


@app.errorhandler(BaseError)
def error_response(error):
    response = make_response(error.message)
    response.status_code = error.status_code
    return response


@app.route('/api')
def hello_world():
    return 'Hello World!'


@app.route('/api/login', methods=['POST'])
def login():
    password = request.form.get('password', '')
    if password != settings.password:
        raise AuthError
    else:
        token = sign_token(120)
        return make_json_response({'token': token})


@app.before_request
def before_request_check():
    if request.method != 'OPTIONS':
        if request.path != '/api/login':
            token = request.headers['Authorization'].split(' ')
            if len(token) < 2:
                raise AuthError
            token = token[1]
            if not verify_token(token):
                raise AuthError


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
