import flask
from flask import request, jsonify
from SentimentClassifier import my_sentiment_analysis

app = flask.Flask(__name__)


@app.route('/api/v1/get-sentiment-for-text', methods=['GET'])
def home():
    text = request.args['text']
    return my_sentiment_analysis(text)

app.run(host='127.0.0.1', port=5001)