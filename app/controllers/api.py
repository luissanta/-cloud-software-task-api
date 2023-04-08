import json
from flask import Blueprint, jsonify, request
from app.services.tasks import TaskService

api_routes = Blueprint('api', __name__)


@api_routes.route('/tasks', methods=['GET'])
def get_tasks():
    max = request.args.get('max', None)
    order = request.args.get('order', None)
    id_user = 1
    service = TaskService()
    return json.dumps(service.get_task(id_user, max, order))

@api_routes.route('/tasks', methods=['POST'])
def create_task():
    file = request.files['file']
    new_format = request.form.get('newFormat', None)
    if new_format is None:
        return "The newFormat is required",400
    name_file = file.filename
    file_data = file.read()
    id_user = 1
    service = TaskService()    
    return json.dumps(service.post_task(id_user, name_file,file_data, new_format))


@api_routes.route('/tasks/<int:id_task>', methods=['GET'])
def get_task(id_task: int):
    service = TaskService()
    return json.dumps(service.get_task_by_id(id_task))


@api_routes.route('/tasks/<int:id_task>', methods=['DELETE'])
def delete_task(id_task: int):
    service = TaskService()
    service.delete_task_by_id(id_task)
    return {}, 204

