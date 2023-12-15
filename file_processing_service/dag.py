from threading import Thread

import requests

from job import ParaphrasingJob, LineCounterJob
from job_status import update_file_ownership, update_file_access, update_job_status

_JOBS = {
    "Paraphrasing": ParaphrasingJob,
    "LineCounter": LineCounterJob
}

# Define dependencies (DAG structure)
_DEPENDENCIES = {
    "Parent": ["Paraphrasing", "LineCounter"]  # Parent depends on Paraphrasing and LineCounter
}


class DAGJobRunner:
    def __init__(self, jobs, dependencies):
        """
        Initialize the DAGJobRunner with jobs and their dependencies.
        :param jobs: A dictionary of job_name: job_instance
        :param dependencies: A dictionary of job_name: [list_of_child_job_names]
        """
        self.jobs = jobs
        self.dependencies = dependencies
        self.completed_jobs = set()
        self.failed_jobs = set()

    def run_job(self, job_name, file_id):
        """
        Run a single job and its dependencies.
        """
        if job_name in self.completed_jobs or job_name in self.failed_jobs:
            # Skip if the job has already been processed
            return

        job = self.jobs[job_name]
        child_jobs = self.dependencies.get(job_name, [])

        threads = []
        for child_job_name in child_jobs:
            thread = Thread(target=self.run_job, args=(child_job_name, file_id))
            threads.append(thread)
            thread.start()

        # Wait for all child jobs to finish
        for thread in threads:
            thread.join()

        # Check if any child job failed
        if any(child in self.failed_jobs for child in child_jobs):
            self.failed_jobs.add(job_name)
            return

        # Run the current job
        job_obj = job(job_name, file_id)
        job_obj.run()
        if job_obj.success:
            self.completed_jobs.add(job_name)
        else:
            self.failed_jobs.add(job_name)

    def run_all(self, file_id: str):
        """
        Run all jobs in the DAG.
        """
        for job_name in self.jobs:
            self.run_job(job_name, file_id=file_id)

        return all(job_name in self.completed_jobs for job_name in self.jobs)


def update_websocket_service(file_id: str, status):
    requests.post("WEBSOCKET_URL", json={"file_id": file_id, "status": status})


def trigger_jobs(file_id, owner_id: int):
    dag_job_runner = DAGJobRunner(_JOBS, _DEPENDENCIES)
    success = dag_job_runner.run_all(file_id)
    print("DAG completed successfully:", success)
    if success:
        update_file_ownership(file_id, owner_id)
        update_file_access(file_id, owner_id)
        update_job_status(file_id, "processed")
        update_websocket_service(file_id, "processed")
    else:
        update_job_status(file_id, "error")
        update_websocket_service(file_id, "error")
