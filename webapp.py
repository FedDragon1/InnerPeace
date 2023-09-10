import numpy as np
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from constants import INDEX_HTML


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def emotion_detection():
    return np.random.rand(7)


@app.route('/api/chat', methods=['POST'])
@cross_origin()
def hello_world():
    emotion_data = emotion_detection()

    return "hello, world"


@app.route('/api/emotion', methods=["POST"])
def get_emotion():
    base64 = request.data


@app.route('/')
def main():
    return open("./frontend/index.html").read()
    return INDEX_HTML


if __name__ == '__main__':
    app.run()
