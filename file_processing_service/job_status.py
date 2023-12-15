import database.query_executor as database_query_executor


def update_job_status(file_id, status) -> None:
    database_query_executor.update_query(query=f"UPDATE files SET status='{status}' WHERE file_id='{file_id}'")


def update_file_ownership(file_id, owner_id):
    database_query_executor.update_query(
        query=f"INSERT INTO file_ownership (file_id, owner_id) VALUES ('{file_id}', '{owner_id}')")


def update_file_access(file_id, user_id):
    database_query_executor.update_query(
        query=f"INSERT INTO file_access (file_id, user_id) VALUES ('{file_id}', '{user_id}')")
