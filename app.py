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
            # Sanitize the input data received with title()
            #   and strip() string methods
            {'category': category.strip().title()},
            {'_id': 1}
        )
        if find_category:
            return jsonify({
                'message': 'Category already exists',
                'status': False
            }), 409
        
        payload = {
            # Sanitize the input data received with title()
            #   and strip() string methods
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
        

@app.route('/categories/<string:category_name>',
        methods=['GET', 'PUT', 'DELETE'])
def get_and_delete_category(category_name):
    if request.method == 'DELETE':
        category = categories.delete_one({
            # We are comparing existing categories with the passed category by
        #   setting it to a title case and replacing all underscores with
        #   spaces so that the category name passed by the user as a dynamic
        #   url parameter would match the category stored in the database
        # For example a category name passed as home_&_accessories would be
        #   mapped with a category of 'Home & accessories
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
        # For any confusions please check the first instance this logic
                #   (category_name.title().replace('_', ' ')) was used in this file
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


@app.route('/categories/<string:category_name>/sub',
        methods=['POST', 'DELETE'])
def create_subcategory(category_name):
    sub_category = request.json.get('sub_category', None)
    if sub_category is None:
        return jsonify({
            'message': 'Required payload ommited',
            'status': False
        }), 400
    
    if request.method == 'POST':        
        if type(sub_category) is not str:
            return jsonify({
                'message': 'The value of sub_category should be a string',
                'status': False
            }), 400
        
        sub = categories.update_one(
            # For any confusions please check the first instance this logic
                #   (category_name.title().replace('_', ' ')) was used in this file
            {'category': category_name.title().replace('_', ' ')},
            {'$push': {
                'sub_category': sub_category.title()
            }}
        )
        if not sub.matched_count:
            return jsonify({
                'message': f"Category {category_name} not found",
                'status': False
            }), 404

        return jsonify({
            'message': 'Subcategory created successfully',
            'status': True
        }), 200
    
    if request.method == 'DELETE':
        if type(sub_category) is not list:
            return jsonify({
                'message': 'The value of sub_category should be a list/array',
                'status': False
            }), 400
        
        success_deletes = []
        failed_deletes = []
        for i in sub_category:
            sub = categories.update_one(
                # For any confusions please check the first instance this logic
                #   (category_name.title().replace('_', ' ')) was used in this file
                {'category': category_name.title().replace('_', ' ')},
                {'$pull': {
                    'sub_category': i.title()
                }}
            )
            if not sub.matched_count:
                return jsonify({
                    'message': f"Category {category_name} not found",
                    'status': False
                }), 404
            
            # If a subcategory cannot be found for deletion add that subcategory
            # to the list of failed deletes
            # Also add successful deletes to the array of successful deletes
            if sub.modified_count:
                success_deletes.append(i)
            else:
                failed_deletes.append(i)

        # This logic is put in place to alert the client of the subcategories
        # which have been deleted and those whose delete operations failed
        fail_message = f'Subcategories not deleted {failed_deletes}'
        fail_status_code = 207
        success_message = f'Deleted subcategories {success_deletes}'
        return jsonify({
            'message': fail_message if len(failed_deletes) else success_message,
            'failure': len(failed_deletes),
            'success': len(success_deletes),
            'total': len(sub_category)
        }), fail_status_code if len(failed_deletes) else 200


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