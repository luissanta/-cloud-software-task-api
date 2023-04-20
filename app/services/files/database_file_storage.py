from sqlalchemy import func
from app.models.models import File
from app.databases import db
from .i_File import IFile

class DatabaseFileStorage(IFile):

    def get(self, id, name, type) -> list:
        pass
    
    def save(self,name_file,file_data) -> int:
        upload_file = File(original_data=file_data, original_name=name_file, created_at=func.now())
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id 