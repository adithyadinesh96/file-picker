class Bucket:
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name

    def upload_file(self, filename: str, file_path: str, stream) -> None:
        """Upload a file to storage """
        print("Upload a file to storage")

    def get_file(self, file_id: str) -> bytes:
        """Download a file from storage """
        print("Download a file from storage")
