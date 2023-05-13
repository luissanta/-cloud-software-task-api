import uuid
from app.models.models import Task, GetTaskSchema, File, PostTaskSchema, GetTaskByIdSchema
from app.databases import db
from app.services.files.file_service import FileService
from app.enums.file import OrderEnum
from app.services.gcp.pubSubTopic import PubSubTopic

task_schema = GetTaskSchema()
post_schema = PostTaskSchema()
get_task_by_id_schema = GetTaskByIdSchema()


class TaskService:
    @classmethod
    def get_task(cls, id_user, max_tasks, order_tasks):
        type_order = OrderEnum.asc if order_tasks is None or order_tasks == '0' else OrderEnum.desc
        if not max_tasks:
            result_query = Task.query.filter(Task.id_user == id_user)\
                .order_by(type_order(Task.id)).all()
        else:
            result_query = Task.query.filter(Task.id_user == id_user)\
                .order_by(type_order(Task.id)).limit(max_tasks).all()

        return [task_schema.dump(task) for task in result_query]

    @classmethod
    def post_task(cls, id_user, name_file, file_data, new_format):
        file_server = FileService()
        pub_sub_topic = PubSubTopic()

        temp_name = name_file.split('.')
        id_file_upload = file_server.send_file(name_file, file_data, new_format)
        new_task = Task(
            id_user=id_user,
            id_original_file=id_file_upload,
            file_name=temp_name[0],
            original_extension=temp_name[1],
            new_extension=new_format,
            status="uploaded",
            task_id=str(uuid.uuid4())
        )
        db.session.add(new_task)
        db.session.commit()
        task_id = new_task.task_id
        url = id_file_upload
        msg = dict(task_id=task_id, url=url, new_format=new_format)
        pub_sub_topic.send_message(msg)
        return post_schema.dump(new_task)

    @classmethod
    def get_task_by_id(cls, id_task):
        result_query = Task.query.filter(Task.task_id == id_task).first()
        return get_task_by_id_schema.dump(result_query)

    @classmethod
    def delete_task_by_id(cls, id_task):
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
        except KeyError:
            result = False
        return result
