from celery_app import celery
from app.models.models import Task
from app.databases import db


@celery.task(name='converter.request')
def converter_request(task_id: str, file_id: int, new_format: str):
    pass


@celery.task(name='converter.response')
def converter_response(task_id, status):
    task = Task.query.filter(Task.task_id == task_id).first()
    if task:
        task.status = status
        db.session.add(task)
        db.session.commit()
  