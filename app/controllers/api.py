import json
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.tasks import TaskService

api_routes = Blueprint('api', __name__)


@api_routes.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    max = request.args.get('max', None)
    order = request.args.get('order', None)
    id_user = get_jwt_identity()
    service = TaskService()
    return json.dumps(service.get_task(id_user, max, order))


@api_routes.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    file = request.files['file']
    new_format = request.form.get('newFormat', None)

    if new_format is None:
        return "The newFormat is required", 400

    name_file = file.filename
    file_data = file.read()
    id_user = get_jwt_identity()
    service = TaskService()    
    return json.dumps(service.post_task(id_user, name_file, file_data, new_format)), 201


@api_routes.route('/tasks/<id_task>', methods=['GET'])
@jwt_required()
def get_task(id_task: str):
    service = TaskService()
    return json.dumps(service.get_task_by_id(id_task))


@api_routes.route('/tasks/<id_task>', methods=['DELETE'])
@jwt_required()
def delete_task(id_task: str):
    service = TaskService()            
    if(service.delete_task_by_id(id_task)):
        return {}, 204
    else:
        return {'response': 'Status not able to be deleted'}, 200


