from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from random import randint


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
        category = request.json.get('category', None)
        sub_category = request.json.get('sub_category', None)

        if not category:
            return jsonify({
                'message': 'Required payload ommited - no title was given',
                'status': False
            }), 400
        
        find_category = categories.find_one(
            {'category': category.strip().title()},
            {'_id': 1}
        ) 
        if find_category:
            return jsonify({
                'message': 'Category already exists',
                'status': False
            }), 409
        
        payload = {
            'category': category.title().strip(),
            'sub_category': sub_category,
            'created_at': datetime.now(),
            'category_id': category.lower().replace(' ', '_') + str(randint(100, 999))
        }
        category = categories.insert_one(payload)
        if category.acknowledged:
            return jsonify({
                'message': 'Category created successfully',
                'status': True,
                'created_id': payload['category_id']
            }), 201
        else:
            return jsonify({
                'message': 'An unexpected error occured',
                'status': False
            }), 500
        
    # Get request
    all = categories.find({}, {'_id': 0})
    all = list(all)
    return jsonify({
        'message': 'Fetched categories successfully',
        'status': True,
        'count': len(all),
        'data': all
    })
        

@app.route(
    '/categories/<string:category_id>',
    methods=['GET', 'PUT', 'DELETE']
)
def RUD_categories(category_id):
    if request.method == 'PUT':
        return 'under construction'
    
    if request.method == 'DELETE':
        return 'under construction'
    
    category = categories.find_one(
        {'category_id': category_id}, {'_id': 0}
    )
    if category is None:
        return jsonify({
            'message': f"Category with category_id {category_id} not found",
            'status': False
        }), 404
        
    return jsonify({
        'message': f"Fetched category ({category_id}) successfully",
        'status': True,
        'data': category
    })


@app.route('/categories/<string:category_id>/sub', methods=['POST'])
def create_subcategory(category_id):
    return 'under construction'


@app.route(
    '/categories/<string:category_id>/sub/<string:subcategory_id>',
    methods=['PUT', 'DELETE']
)
def UD_subcategory(category_id, subcategory_id):
    return 'under construction'


@app.route('/')
def index():
    return jsonify({
        'message': 'CRUD APIs for tencowry categories'
    })


if __name__ == '__main__':
    app.run(debug=True)