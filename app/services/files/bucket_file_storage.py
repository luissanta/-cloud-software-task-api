from app.enums.file import FileTypeEnum
from app.models.models import File
from app.databases import db
from .i_File import IFile
import os
from google.cloud import storage

path = os.path.join(os.getcwd(), os.environ.get('GCP_PATH'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
storage_client = storage.Client(path)
bucket = storage_client.get_bucket(os.environ.get('GCP_BUCKET'))


class BucketFileStorage(IFile):
    def save(self, file_name, file_data, new_format) -> int:
        blob = bucket.blob(file_name)
        blob.upload_from_string(file_data)

        upload_file = File(
            original_name=file_name,
            new_format=new_format
        )
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id

    def get(self):
        pass