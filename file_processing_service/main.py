import time

import database.query_executor as database_query_executor
from dag import trigger_jobs


def fetch_next_job():
    jobs = database_query_executor.select_query(
        query=f"SELECT * FROM files WHERE status = 'downloaded' ORDER BY created_at ASC LIMIT 1")
    if jobs:
        return jobs[0]
    return None


def main():
    while True:
        job = fetch_next_job()
        if job:
            trigger_jobs(file_id=job[0], owner_id=job[1])
        else:
            # No more jobs or wait before retrying
            time.sleep(5)

if __name__ == '__main__':
    main()