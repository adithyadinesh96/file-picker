from typing import List

import database.query_executor as database_query_executor


def update_job_status(file_id, status) -> None:
    database_query_executor.update_query(query=f"UPDATE files SET status = '{status}' WHERE file_id = '{file_id}'")


def get_earliest_pending_download_jobs(limit=5) -> List:
    return database_query_executor.select_query(
        query=f"SELECT * FROM files WHERE status = 'created' ORDER BY created_at ASC LIMIT {limit}")
