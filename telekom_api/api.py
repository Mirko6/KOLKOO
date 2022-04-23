import flask
from flask import request, jsonify

app = flask.Flask(__name__)


@app.route('/api/v1/get-sentiment-for-text', methods=['GET'])
def home():
    text = request.args['text']
    return text

app.run(host='127.0.0.1', port=5001)