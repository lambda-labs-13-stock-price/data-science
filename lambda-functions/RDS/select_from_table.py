import logging
from create_tables.py import  make_conn, fetch


def lambda_handler(event, context):
    SQL_cmd = "SELECT COUNT(\*) FROM tweets"
    print(SQL_cmd)

    conn = make_conn()
    result = fetch(conn,SQL_cmd)

    conn.close()

    return result