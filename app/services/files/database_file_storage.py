from enum import Enum
from sqlalchemy import func
from app.models.models import File
from app.databases import db
from .i_File import IFile

class FileTypeEnum(Enum):
    ORIGINAL = 'ORIGINAL'
    COMPRESSED = 'COMPRESSED'

class DatabaseFileStorage(IFile):

    def extract_name(self, file, type):        
        if type  == FileTypeEnum.ORIGINAL.value:
            return file.original_name, file.original_data
        else:
            tmp_name = file.original_name
            tmp_name = tmp_name.split('.')
            tmp_name = tmp_name+"."+file.new_format
            return tmp_name,  file.compressed_data
        
    def get(self, id, type) -> tuple:
        fetched_file = File.query.get_or_404(id)
        name, data = self.extract_name(fetched_file, type)
        return data , name       
    
    def save(self,name_file,file_data, new_format) -> int:
        upload_file = File(original_data=file_data, original_name=name_file, created_at=func.now(), new_format = new_format)
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id 