import logging
import threading

from download import handle_job_download
from job import get_earliest_pending_download_jobs


def download_service_main_loop():
    while True:
        try:
            jobs = get_earliest_pending_download_jobs()
            threads = []
            for job in jobs:
                thread = threading.Thread(target=handle_job_download, args=(job,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()
        except Exception as e:
            logging.error(f"Issue in Downloading Files{e}")

if __name__ == '__main__':
    download_service_main_loop()