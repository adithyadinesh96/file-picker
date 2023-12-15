from abc import ABC, abstractmethod


class Job(ABC):
    """
    Abstract base class for jobs. All job types must implement the run method.
    """

    def __init__(self, name, file_id: str):
        self.name = name
        self.file_id = file_id
        self.success = None

    @abstractmethod
    def run(self):
        """
        The logic for the job execution. Must be implemented by all subclasses.
        """
        pass


class ParaphrasingJob(Job):
    def run(self):
        try:
            print(f"Running data Paraphrasing job: {self.name} for file {self.file_id}")
            # Data processing logic
            self.success = True
        except Exception as e:
            print(f"Paraphrasing job {self.name} failed: {e} for file {self.file_id}")
            self.success = False


class LineCounterJob(Job):
    def run(self):
        try:
            print(f"LineCounter job: {self.name} for file {self.file_id}")
            # Network request logic
            self.success = True
        except Exception as e:
            print(f"LineCounter job {self.name} failed: {e} for file {self.file_id}")
            self.success = False

# ... Add more job types as needed ...
