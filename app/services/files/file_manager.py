from typing import final
from app.services.files import IFile

class FileManager:
    __manager = None
    def __init__(self, manager: IFile) -> None:
        self.__manager = manager
        super().__init__()
    
    @final
    def get_file(self, id, type):
        return self.__manager.get(id, type)

    @final
    def save_file(self, name, file, new_format):
        return self.__manager.save(name, file, new_format)
    