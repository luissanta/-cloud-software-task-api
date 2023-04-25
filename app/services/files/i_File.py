from abc import ABC, abstractmethod


class IFile(ABC):

    @abstractmethod
    def get(self, file_id, file_type) -> tuple:
        pass

    @abstractmethod
    def save(self, name, file, new_format) -> int:
        pass
