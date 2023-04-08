from sqlalchemy import func
from celery_app import celery
from app.models.models import Task
from app.databases import db

@celery.task(name='converter.request')
def converter_request(task_id, url):
    pass


@celery.task(name='converter.response')
def converter_response(task_id, status):
    task = Task.query.filter(Task.task_id == task_id).first()
    if task:
        task.updated_at = func.now()
        task.status = status
        db.session.delete(task)
        db.session.commit()
  