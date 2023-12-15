from typing import Optional

import database.query_executor as database_query_executor


def grant_file_access(file_id, grantee_user_id):
    database_query_executor.update_query(
        query=f"INSERT INTO file_access (file_id, user_id) VALUES ('{file_id}', {grantee_user_id})")


def can_grantor_give_access(grantor_user_id, file_id) -> bool:
    try:
        rows = database_query_executor.select_query(
            query=f"SELECT owner_id FROM file_ownership WHERE file_id = '{file_id}' and owner_id = '{grantor_user_id}'")
        if rows and rows[0][0] == grantor_user_id:
            return True
    except Exception:
        return False
    return False


def user_has_access_to_file(user_id, file_id) -> bool:
    rows = database_query_executor.select_query(
        query=f"SELECT * FROM file_access WHERE user_id = {user_id} AND file_id = '{file_id}'")
    return len(rows) > 0


def get_file(file_id, user_id) -> Optional[tuple]:
    files = database_query_executor.select_query(
        f"SELECT * FROM files WHERE file_id = '{file_id}' and user_id = {user_id}")
    if files:
        return files[0]
    return None
