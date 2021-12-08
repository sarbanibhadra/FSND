import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():

    all_drinks = Drink.query.all()
    drinks = {}

    if len(all_drinks) == 0:  
        abort(404)
   

    for d in all_drinks:
        drinks = [d.short()]

    return jsonify({
        "success": True, 
        "drinks": drinks
    }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    print("drinks -details")
    all_drinks = Drink.query.all()

    drinks = {}

    if all_drinks is None:  
        abort(404)

    for d in all_drinks:
        drinks = [d.long()]

    return jsonify({
        'success': True,
        'drinks': drinks
    }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    request_bar = request.get_json()
    title = request_bar.get('title', None)
    print(title)
    recipe = request_bar.get('recipe', None)
    print(recipe)
    if request_bar is null:
        abort(400)
    try:
        new_drink = Drink(title = title, recipe = json.dumps(recipe))
        new_drink.title = title
        new_drink.recipe =  json.dumps(recipe)
        new_drink.insert()
        new_drink = [new_drink.long()]
        return jsonify({'success': True, 'drinks': new_drink}), 200
    except:
        return json.dumps({'success': False, 'error': "An error occurred" }), 500

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_the_drink_id(payload, id):
    request_bar = request.get_json()
    drink = Drink()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)

    try:
        print(request_bar)
        if request_bar['title'] is not None:
            drink.title = request_bar['title']
        
        if request_bar.get('recipe') is not None:
            drink.recipe =  json.dumps([request_bar['recipe']])
               
        drink.update()
        drink = [drink.long()]
        return jsonify({'success': True, 'drinks': drink}), 200

    except:
        return json.dumps({'success': False, 'error': "An error occurred" }), 500 



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    print("inside delete")
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
        return jsonify({'success': True, 'delete': id}), 200

    except:
        return json.dumps({'success': False, 'error': "An error occurred" }), 500

    

'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    print(error)
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405

@app.errorhandler(403)
def permission_not_present(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": 'Permission Not Present'
    }), 403    

@app.errorhandler(500)
def error_present(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'An error occurred'
    }), 500