from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskdb'
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def index():
    return '<h1>Hola mundo desde Flask!</h1>'

@app.route('/tasks', methods=['GET'])
def get_tasks_list():
    tasks = mongo.db.tasks.find()
    response = json_util.dumps(tasks)
    return Response(response, mimetype='application/json')

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(task)
    return Response(response, mimetype='application/json')

@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']

    if title and description:
        id = mongo.db.tasks.insert_one(
            {'title': title, 'description': description}
        )
        response = jsonify({'message': 'New task created successfully'})
        return response
    else:
        return {'error': 'must fill all of the fields'}

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    title = request.json['title']
    description = request.json['description']

    if title and description:
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {
            'title': title,
            'description': description
        }})
        response = jsonify({'message': f'Task with id: {id} was updated successfully'})
        return response

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    mongo.db.tasks.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': f'Task with id: {id} was deleted successfully'})
    return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)