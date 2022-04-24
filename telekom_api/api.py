import flask
from flask import request, jsonify
from flask_cors import CORS
from SentimentClassifier import my_sentiment_analysis

app = flask.Flask(__name__)
CORS(app)

@app.route('/api/v1/get-sentiment-for-text', methods=['GET'])
def home():
    text = request.args['text']
    return jsonify({'hate': 1 if my_sentiment_analysis(text) else 0})

app.run(host='127.0.0.1', port=5001)