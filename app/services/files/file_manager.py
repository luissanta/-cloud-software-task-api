from typing import final
from app.services.files import IFile


class FileManager:
    __manager = None

    def __init__(self, manager: IFile) -> None:
        self.__manager = manager
        super().__init__()

    @final
    def get_file(self, file_id, file_type):
        return self.__manager.get(file_id, file_type)

    @final
    def save_file(self, file_name, file_data, new_format):
        return self.__manager.save(file_name, file_data, new_format)
