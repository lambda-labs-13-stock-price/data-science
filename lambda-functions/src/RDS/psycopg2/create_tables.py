import logging
from db_utils import *
from SQL_utils import create_tweets_table

# Lambda function to create tweets table if it does not exist

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    SQL_cmd = create_tweets_table

    print(SQL_cmd)

    conn = make_conn()
    result = fetch(conn,SQL_cmd)

    conn.close()

    return result