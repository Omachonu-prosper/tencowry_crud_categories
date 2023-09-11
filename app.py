from flask import Flask, jsonify
from pymongo import MongoClient


app = Flask(__name__)

# MongoDB configuration and instantiation
client = MongoClient('mongodb://localhost:27017')
db = client['test']
categories = db['categories']


@app.route('/')
def index():
    return jsonify({
        'message': 'CRUD APIs for tencowry categories'
    })


if __name__ == '__main__':
    app.run(debug=True)