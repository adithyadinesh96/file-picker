from datetime import datetime

import database.query_executor as database_query_executor


def create_job(file_id, user_id, drive_name) -> None:
    database_query_executor.update_query(
        query=f"INSERT INTO files (file_id, user_id, status, created_at, drive_name) VALUES ('{file_id}', {user_id}, 'created', to_timestamp({datetime.now().timestamp()}), '{drive_name}')")
