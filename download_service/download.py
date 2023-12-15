import logging

import drive.factory as drive_factory
from bucket import Bucket
from job import update_job_status


def handle_job_download(job: tuple):
    file_id, user_id, status, created_at, drive_name = job
    try:
        update_job_status(file_id, "downloading")
        drive = drive_factory.get_drive(drive_name=drive_name)
        file_stream = drive().download_file(file_id)
        Bucket("BUCKET_NAME").upload_file(file_stream, file_id)
        update_job_status(file_id, "downloaded")
    except Exception as e:
        logging.error(e)
        update_job_status(file_id, "error")
