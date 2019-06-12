import logging
from SQL_utils import select_all_from_table
from create_tables import  make_conn, fetch

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    SQL_cmd = select_all_from_table
    print(SQL_cmd)

    conn = make_conn()
    result = fetch(conn,SQL_cmd)

    conn.close()

    return result