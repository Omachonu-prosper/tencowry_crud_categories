import os

from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)

load_dotenv()
CORS()

try:
    # If we are working in a production environment (deployed state)
    # the database to be used will be the mongodb atlas database
    # else the local mongodb instance will be used
    app_status = os.environ.get('APP_STATUS')
    if app_status == 'production':
        db_username = os.environ['DATABASE_USER']
        db_passwd = os.environ['DATABASE_PASSWORD']
        db_url = os.environ['DATABASE_URL']
        uri = f"mongodb+srv://{db_username}:{db_passwd}@{db_url}"
    else:
        uri = "mongodb://127.0.0.1:27017"
except Exception as e:
    print(f'Error in connection to Database: {e}')

client = MongoClient(uri)
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
                'message': 'Required payload ommited',
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
    all = list(all)
    return jsonify({
        'message': 'Fetched categories successfully',
        'status': True,
        'count': len(all),
        'data': all
    })
        

@app.route(
    '/categories/<string:category_name>',
    methods=['GET', 'PUT', 'DELETE']
)
def RUD_categories(category_name):
    # The name RUD is gotten from CRUD just without a C
    if request.method == 'PUT':
        category = request.json.get('category', None)
        sub_category = request.json.get('sub_category', None)
        
        if not sub_category:
            return jsonify({
                'message': 'Required payload ommited - no sub_category was given',
                'status': False
            }), 400
        
        new_sub_category = categories.update_one(
             {'category': category_name.title().replace('_', ' ')},
             {'$set': {
                  'sub_category': sub_category
             }}
        )
        if not new_sub_category.matched_count:
            return jsonify({
                'message': f"Category {category_name} not found",
                'status': False
            }), 400

        if category:
            update_category = categories.update_one(
                {'category': category_name.title().replace('_', ' ')},
                {'$set': {
                    'category': category
                }}
            )
            if not update_category.matched_count:
                return jsonify({
                    'message': f"Category {category_name} not found",
                    'status': False
                }),
            
        return jsonify({
            'message': f"Category {category_name} updated successfully",
            'status': True
        }), 200

    if request.method == 'DELETE':
        category = categories.delete_one({
            'category': category_name.title().replace('_', ' ')
        })
        if category.deleted_count:
            return jsonify({
                'message': f"Category {category_name} deleted successfully",
                'status': True
            }), 200
        else:
            return jsonify({
                'message': f"Category {category_name} not found",
                'status': False
            }), 404
    
    category = categories.find_one(
        {'category': category_name.title().replace('_', ' ')},
        {'_id': 0}
    )
    if category is None:
        return jsonify({
            'message': f"Category {category_name} not found",
            'status': False
        }), 404
        
    return jsonify({
        'message': f"Fetched category ({category_name}) successfully",
        'status': True,
        'data': category
    })


@app.route('/categories/<string:category_name>/sub', methods=['POST'])
def create_subcategory(category_name):
    sub_category = request.json.get('sub_category', None)
    if sub_category is None:
        return jsonify({
            'message': 'Required payload ommited',
            'status': False
        }), 400
    
    if type(sub_category) is not str:
        return jsonify({
            'message': 'The value of sub_category should be a string',
            'status': False
        }), 400
    
    sub = categories.update_one(
        {'category': category_name.title().replace('_', ' ')},
        {'$push': {
            'sub_category': sub_category
        }}
    )
    if not sub.matched_count:
        return jsonify({
            'message': f"Category {category_name} not found",
            'status': False
        }), 404

    return jsonify({
        'message': 'Subcategory created successfully',
        'status': False
    }), 200


@app.route(
    '/categories/<string:category_name>/sub/<string:subcategory_name>',
    methods=['PUT', 'DELETE']
)
def UD_subcategory(category_name, subcategory_name):
    return 'under construction'


@app.route('/')
def index():
    return jsonify({
        'message': 'CRUD APIs for tencowry categories'
    }), 200


if __name__ == '__main__':
	if os.environ.get('APP_STATUS') == 'production':
		app.run()
	else:
		app.run(debug=True)