

from app.models.models import GetTaskSchema,PostTaskSchema, GetTaskByIdSchema
from .file_manager import FileManager
from app.services.files.network_file_storage import NetworkFileStorage
task_schema = GetTaskSchema()
post_schema = PostTaskSchema()
get_task_by_id_schema = GetTaskByIdSchema()
reporting_service = FileManager(NetworkFileStorage())
class FileService:
    def get_file(self,name, file):        
        reporting_service.get_file(name, file)
   
    def send_file(self,name, file):        
        return reporting_service.save_file(name, file)