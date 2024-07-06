"""
CI/CD pipeline is created for this application using cloud build to deploy on GCP cloud run
check
"""
import os
from flask import Flask, jsonify, request, abort

# Create a Flask application
app = Flask(__name__)

# Define a route and its handler
@app.route('/')
def hello():
    return 'Hello, World! Welcome to GCP CI/CD with Cloud Build'

# Sample data - Replace this with a database in a real application
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'}
]

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

# Route to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify({'user': user})
    else:
        abort(404, f'User with ID {user_id} not found')

# Route to create a new user
@app.route('/createusers', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json:
        abort(400, 'Name is required in request JSON')
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name']
    }
    users.append(user)
    return jsonify({'user': user}), 201

# Route to update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        abort(404, f'User with ID {user_id} not found')
    if not request.json:
        abort(400, 'Request JSON is empty')
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400, 'Name must be a string')
    user['name'] = request.json.get('name', user['name'])
    return jsonify({'user': user}), 200

# Route to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        abort(404, f'User with ID {user_id} not found')
    users.remove(user)
    return jsonify({'result': True}), 200

# Run the application if this file is executed directly
if __name__ == '__main__':
    print(" Starting app...")
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)

