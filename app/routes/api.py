from flask import Blueprint, jsonify, request

api_routes = Blueprint('api', __name__)


@api_routes.route('/tasks', methods=['GET'])
def get_tasks():
    max = request.args.get('max', None)
    order = request.args.get('order', None)
    print(max)
    print(order)
    if max is None:
        # the page parameter was not given in the request, handle it accordingly
        pass
    else:
        pass
        # page parameter was in the request, handle it accordingly
    return [{
        'id': 1,
        'fileName': 'https://drive.google.com/drive/u/1/folders/1iUJ-QtDmzi1VMGTxLeluoRDgvXGUb5uH',
        'originalExtension': 'doc',
        'newExtension': 'zip',
        'status': 'pending'
    }], 200


@api_routes.route('/tasks', methods=['POST'])
def create_task():
    return {'id': 1, 'status': 'uploaded'}, 201


@api_routes.route('/tasks/<int:id_task>', methods=['GET'])
def get_task(id_task: int):
    return {
        'id': id_task,
        'fileName': 'https://drive.google.com/drive/u/1/folders/1iUJ-QtDmzi1VMGTxLeluoRDgvXGUb5uH',
        'status': 'pending'
    }, 200


@api_routes.route('/tasks/<int:id_task>', methods=['DELETE'])
def delete_task(id_task: int):
    return {}, 204
