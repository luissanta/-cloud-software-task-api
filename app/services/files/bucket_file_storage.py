from app.enums.file import FileTypeEnum
from app.models.models import File
from app.databases import db
from .i_File import IFile
import uuid
import os
from google.cloud import storage
from app.data_transfer_objects.file import FileTypeDTO

path = os.path.join(os.getcwd(), os.environ.get('GCP_PATH'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
storage_client = storage.Client(path)
bucket = storage_client.get_bucket(os.environ.get('GCP_BUCKET'))


class BucketFileStorage(IFile):
    def save(self, file_name, file_data, new_format) -> int:
        temporal_name = str(uuid.uuid4())
        temp_original_name = file_name.split('.')
        blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_ORIGINAL') + '/' +
                           temporal_name + "." +
                           temp_original_name[1])
        blob.upload_from_string(file_data)

        upload_file = File(
            original_name=file_name,
            new_format=new_format,
            temporal_name=temporal_name
        )
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id

    def get(self, file_id, file_type: FileTypeDTO) -> tuple:
        fetched_file = File.query.get_or_404(file_id)

        if file_type.file_type == FileTypeEnum.ORIGINAL.value:
            blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_ORIGINAL') + '/' + fetched_file.original_name)
        else:
            blob = bucket.blob(os.environ.get('GCP_BUCKET_PATH_COMPRESSED') + '/' + fetched_file.original_name)

        data = blob.download_as_bytes()
        return data, fetched_file.original_name
