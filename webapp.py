from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from constants import INDEX_HTML


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/chat', methods=['POST'])
@cross_origin()
def hello_world():
    print(request)
    return "hello, world"


@app.route('/')
def main():
    return INDEX_HTML


if __name__ == '__main__':
    app.run()
