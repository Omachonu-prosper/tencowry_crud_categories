from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)

# MongoDB configuration and instantiation
client = MongoClient('mongodb://localhost:27017')
db = client['test']
categories = db['categories']


@app.route('/categories', methods=['POST', 'GET'])
def get_create_categories():
    # Post request
    if request.method == 'POST':
        """
        Workflow
        - Gets the payload
        - Return errors if required payloads are ommited
        - Return errors if category already exists
        - Create category if requirements are met
        - Notify user on the status of the operation
        """
        title = request.json.get('title', None)
        sub_categories = request.json.get('sub-categories', None)

        if not title:
            return jsonify({
                'message': 'Required payload ommited - no title was given',
                'status': False
            }), 400
        
        find_category = categories.find_one(
            {'title': title.strip().title()},
            {'_id': 1}
        ) 
        if find_category:
            return jsonify({
                'message': 'Category already exists',
                'status': False
            }), 409
        
        payload = {
            'title': title.title().strip(),
            'sub_categories': sub_categories,
            'created_at': datetime.now()
        }
        category = categories.insert_one(payload)
        if category.acknowledged:
            return jsonify({
                'message': 'Category created successfully',
                'status': True
            }), 201
        else:
            return jsonify({
                'message': 'An unexpected error occured',
                'status': False
            }), 500
        
    # Get request
    all = categories.find({}, {'_id': 0})
    return jsonify({
        'message': 'Fetched categories successfully',
        'status': True,
        'data': list(all)
    })
        

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