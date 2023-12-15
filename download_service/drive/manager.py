from abc import abstractmethod
from typing import List


class DriveManager:
    @abstractmethod
    def download_file(self, file_id: str):
        pass

    @abstractmethod
    def list_files(self, path: str) -> List[str]:
        pass

    @abstractmethod
    def is_exists(self, path: str) -> bool:
        pass
