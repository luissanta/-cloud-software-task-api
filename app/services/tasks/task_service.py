from enum import Enum
import json

from sqlalchemy import desc, asc, func
from app.models.models import Task, GetTaskSchema, Upload,PostTaskSchema, GetTaskByIdSchema
from app.databases import db
from app.celery.tasks_celery import converter_request

task_schema = GetTaskSchema()
post_schema = PostTaskSchema()
get_task_by_id_schema = GetTaskByIdSchema()
class TaskService:
    def get_task(self,id_user, max, order):
        typeOrder =  orderby.asc if order == None or order == '0' else orderby.desc
        if not max:
            result_query = Task.query.filter(Task.id_user == id_user).order_by(typeOrder(Task.id)).all()
        else:
            result_query = Task.query.filter(Task.id_user == id_user).order_by(typeOrder(Task.id)).limit(max).all()
        
        return [task_schema.dump(task) for task in result_query]
    
    def post_task(self,id_user, name_file,file_data, new_format):
        upload_file = Upload(data=file_data, filename=name_file, created_at=func.now())
        db.session.add(upload_file)
        db.session.commit()
        temp_name = name_file.split('.')
        new_task = Task(id_user=id_user,id_original_file=upload_file.id,file_name=temp_name[0], original_extension= temp_name[1] , new_extension=new_format, status="uploaded", created_at=func.now() )
        db.session.add(new_task)
        db.session.commit()
        task_id = new_task.task_id
        url = upload_file.id
        args = (task_id, url,)
        converter_request.apply_async(args=args, queue='request')
        return post_schema.dump(new_task)
    
    def get_task_by_id(self, id_task):
        result_query = Task.query.filter(Task.id == id_task).all()
        return [get_task_by_id_schema.dump(task) for task in result_query]
    
    def delete_task_by_id(self, id_task):
        task = Task.query.filter(Task.id == id_task).first()
        result = False
        if task:
            db.session.delete(task)
            db.session.commit()
            original_file = Upload.query.filter(Upload.id == task.id_original_file).first()
            if original_file:
                db.session.delete(original_file)
                db.session.commit()
            result = True
        return {'Deleted': result}
    
class orderby(Enum):
    desc = desc
    asc = asc