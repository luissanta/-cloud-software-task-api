from sqlalchemy import func
from app.models.models import File
from app.databases import db
from .i_File import IFile
from app.enums.file import FileTypeEnum


class DatabaseFileStorage(IFile):
    @classmethod
    def extract_name(cls, file, type_file):
        if type_file == FileTypeEnum.ORIGINAL.value:
            return file.original_name, file.original_data
        else:
            tmp_name = file.original_name
            tmp_name = tmp_name.split('.')
            tmp_name = tmp_name + "." + file.new_format
            return tmp_name,  file.compressed_data

    def get(self, file_id, type_file) -> tuple:
        fetched_file = File.query.get_or_404(file_id)
        name, data = self.extract_name(fetched_file, type_file)
        return data, name

    def save(self, file_name, file_data, new_format) -> int:
        upload_file = File(
            original_data=file_data,
            original_name=file_name,
            created_at=func.now(),
            new_format=new_format
        )
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id
