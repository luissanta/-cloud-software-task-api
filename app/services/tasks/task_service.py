from enum import Enum
import uuid
from sqlalchemy import desc, asc, func
from app.models.models import Task, GetTaskSchema, File, PostTaskSchema, GetTaskByIdSchema
from app.databases import db
from app.celery.tasks_celery import converter_request
from app.services.files.file_service import FileService

task_schema = GetTaskSchema()
post_schema = PostTaskSchema()
get_task_by_id_schema = GetTaskByIdSchema()


class TaskService:
    def get_task(self, id_user, max, order):
        type_order = OrderBy.asc if order is None or order == '0' else OrderBy.desc
        if not max:
            result_query = Task.query.filter(Task.id_user == id_user).order_by(type_order(Task.id)).all()
        else:
            result_query = Task.query.filter(Task.id_user == id_user).order_by(type_order(Task.id)).limit(max).all()

        return [task_schema.dump(task) for task in result_query]

    def post_task(self, id_user, name_file, file_data, new_format):

        file_server = FileService()
        temp_name = name_file.split('.')
        id_file_upload = file_server.send_file(name_file, file_data, new_format)
        new_task = Task(
            id_user=id_user,
            id_original_file=id_file_upload,
            file_name=temp_name[0],
            original_extension=temp_name[1],
            new_extension=new_format, status="uploaded",
            created_at=func.now(),
            task_id=str(uuid.uuid4())
        )
        db.session.add(new_task)
        db.session.commit()
        task_id = new_task.task_id
        url = id_file_upload
        # args = (task_id, url, new_format,)
        # converter_request.apply_async(args=args, queue='request')
        return post_schema.dump(new_task)

    def get_task_by_id(self, id_task):
        result_query = Task.query.filter(Task.task_id == id_task).first()
        return get_task_by_id_schema.dump(result_query)

    def delete_task_by_id(self, id_task):
        result = False
        try:
            task = Task.query.filter(Task.task_id == id_task).first()
            if task and task.status.lower() == 'processed':
                db.session.delete(task)
                db.session.commit()
                original_file = File.query.filter(File.id == task.id_original_file).first()
                if original_file:
                    db.session.delete(original_file)
                    db.session.commit()
                result = True
        except:
            result = False
        return result


class OrderBy(Enum):
    desc = desc
    asc = asc
