from io import BytesIO
import uuid
from sqlalchemy import func
from app.models.models import File
from app.databases import db
from smb.SMBConnection import SMBConnection
from .i_File import IFile
import os
from app.enums.file import FileTypeEnum


class NetworkFileStorage(IFile):
    smb_username = os.getenv("SMB_USERNAME", "")
    smb_password = os.getenv("SMB_PASSWORD", "")
    smb_server_ip = os.getenv("SMB_SERVER_IP", "")
    smb_folder_name = os.getenv("SMB_FORDER_NAME", "")

    def extract_name(self, file, type_file):
        if type_file.file_type == FileTypeEnum.ORIGINAL.value:
            name = file.original_name.split('.')
            return file.original_name, "\\public\\original\\", name[1]
        else:
            tmp_name = file.original_name
            tmp_name = tmp_name.split('.')
            tmp_name = tmp_name[0] + "." + file.new_format
            return tmp_name, "\\public\\compressed\\", file.new_format

    def get(self, file_id, file_type) -> tuple:
        fetched_file = File.query.get_or_404(file_id)
        original_name, path, extension = self.extract_name(fetched_file, file_type)
        conn = SMBConnection(
            self.smb_username,
            self.smb_password,
            remote_name='',
            my_name='',
            use_ntlm_v2=True,
            is_direct_tcp=True
        )
        conn.connect(self.smb_server_ip, 445)
        memoria = BytesIO()
        memoria.seek(0)
        data = memoria.read()
        memoria.close()
        conn.close()

        return data, original_name

    def save(self, name_file, file_data, new_format) -> int:
        temporal_name = str(uuid.uuid4())
        temp_original_name = name_file.split('.')
        conn = SMBConnection(
            self.smb_username,
            self.smb_password,
            remote_name='',
            my_name='',
            use_ntlm_v2=True,
            is_direct_tcp=True
        )
        try:
            conn.connect(self.smb_server_ip, 445)
            conn.storeFile(self.smb_folder_name, "\\public\\original\\" + temporal_name + "." + temp_original_name[1],
                           BytesIO(file_data))
        except Exception as e:
            print(f"Detail error: {e}")

        conn.close()
        upload_file = File(original_name=name_file, created_at=func.now(), temporal_name=temporal_name,
                           new_format=new_format)
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id
