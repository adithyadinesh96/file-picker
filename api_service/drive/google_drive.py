from typing import List

from drive.manager import DriveManager


class GoogleDriveManager(DriveManager):

    def download_file(self, file_id: str):
        pass

    def list_files(self, path: str) -> List[str]:
        results = {}  # Fetch actual results from Drive
        files = results.get('files', [])
        return files

    def is_exists(self, path: str) -> bool:
        pass
