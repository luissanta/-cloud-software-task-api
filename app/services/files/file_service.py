from app.models.models import GetTaskSchema, PostTaskSchema, GetTaskByIdSchema
from .file_manager import FileManager
from app.services.files.bucket_file_storage import BucketFileStorage
from app.data_transfer_objects.file import FileTypeDTO

task_schema = GetTaskSchema()
post_schema = PostTaskSchema()
get_task_by_id_schema = GetTaskByIdSchema()
file_manager = FileManager(BucketFileStorage())


class QueryParamsRequired(Exception):
    pass


class FileService:
   
    def send_file(self, name, file, new_format):
        return file_manager.save_file(name, file, new_format)

    def validate_get_file(self, file_type: FileTypeDTO) -> None:
        if not file_type.file_type:
            raise QueryParamsRequired('The type parameters is required')

    def get_file(self, file_id: int, file_type: FileTypeDTO):
        data, name = file_manager.get_file(file_id, file_type)
        return data, name
