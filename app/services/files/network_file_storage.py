from io import BytesIO
import uuid

from sqlalchemy import func
from app.models.models import File
from app.databases import db
from smb.SMBConnection import SMBConnection  
from .i_File import IFile
import os

class NetworkFileStorage(IFile):

    def get(self,id, name, type) -> list:
        pass
    
    def save(self,name_file,file_data) -> list:
        
        
        smb_username = os.getenv("smb_username", "")
        smb_password =  os.getenv("smb_password", "")
        smb_server_ip = os.getenv("smb_server_ip", "") 
        smb_folder_name = os.getenv("smb_folder_name", "")
        
        temporal_name = str(uuid.uuid4())
        temp_original_name = name_file.split('.')
        conn = SMBConnection(smb_username, smb_password,remote_name='',my_name='', use_ntlm_v2=True, is_direct_tcp=True)
        try:            
            conn.connect(smb_server_ip, 445)            
            conn.storeFile(smb_folder_name, "\\public\\original\\"+temporal_name+"."+temp_original_name[1],BytesIO(file_data))            
        except Exception as e:
           print(f"Detail error: {e}")

        conn.close()
        upload_file = File(original_name=name_file, created_at=func.now(), temporal_name = temporal_name)
        db.session.add(upload_file)
        db.session.commit()
        return upload_file.id  