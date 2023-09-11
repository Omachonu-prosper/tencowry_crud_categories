from flask import Flask, jsonify
from pymongo import MongoClient


app = Flask(__name__)

# MongoDB configuration and instantiation
client = MongoClient('mongodb://localhost:27017')
db = client['test']
categories = db['categories']


@app.route('/categories', methods=['POST', 'GET'])
def get_create_categories():
    return 'under construction'


@app.route(
    '/categories/<string:category_title>',
    methods=['GET', 'PUT', 'DELETE']
)
def RUD_categories(category_title):
    return 'under construction'


@app.route('/categories/<string:category_title>/sub', methods=['POST'])
def create_subcategory(category_title):
    return 'under construction'


@app.route(
    '/categories/<string:category_title>/sub/<string:subcategory_title>',
    methods=['PUT', 'DELETE']
)
def UD_subcategory(category_title, subcategory_title):
    return 'under construction'


@app.route('/')
def index():
    return jsonify({
        'message': 'CRUD APIs for tencowry categories'
    })


if __name__ == '__main__':
    app.run(debug=True)