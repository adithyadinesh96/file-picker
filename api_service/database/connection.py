import psycopg2


def get_db_connection():
    conn = psycopg2.connect('CONNECTION_STR')
    return conn
