from enum import Enum
import json

from sqlalchemy import desc, asc
from app.models.models import Task, GetTaskSchema

task_schema = GetTaskSchema()
class TaskService:
    def get_task(self,id_user, max, order):
        typeOrder =  orderby.asc if order == None or order == '0' else orderby.desc
        if not max:
            result_query = Task.query.filter(Task.id_user == id_user).order_by(typeOrder(Task.id)).all()
        else:
            result_query = Task.query.filter(Task.id_user == id_user).order_by(typeOrder(Task.id)).limit(max).all()
        
        return [task_schema.dump(task) for task in result_query]
    
class orderby(Enum):
    desc = desc
    asc = asc