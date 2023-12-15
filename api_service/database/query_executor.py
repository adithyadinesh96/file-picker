from typing import List

from database.connection import get_db_connection


def update_query(query: str):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print(f"Error Running Query {query} {e}")
    finally:
        cur.close()
        conn.close()


def select_query(query: str) -> List:
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        print(f"Error Running Query {query} {e}")
