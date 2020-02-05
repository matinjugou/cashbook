from utils import *
from views.cashbook import cashbook
import settings

from flask import Flask, make_response
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


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
