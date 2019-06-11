import psycopg2
import logging
import sys
from subprocess import call

db_host = call("aws rds describe-db-instances | jq -r '.DBInstances[]|select(.DBInstanceIdentifier=='rds-reddit-data').Endpoint|.Address'", shell=True)
db_port = 5432
db_name = "hiddenalphabet_reddit_data"
db_user = "hiddenalphabet"
db_pass = "hiddenalphabet"
db_table = "?"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name,db_user,db_host,db_pass))
    except:
        logger.error("Unexpected error: Could not connect to RDS-PostgreSQL instance")

    return conn

def fetch(conn,query):
    result = []
    print('Executing Query : %s' % (query))

    cursor = conn.cursor()
    cursor.execute(query)
    raw = cursor.fetchall()

    for line in raw:
        result.append(line)

    return result

# Lambda function to create tweets table if it does not exist

def lambda_handler(event, context):
    SQL_cmd = "CREATE TABLE IF NOT EXISTS tweets (
              id int primary key,
              tweet_id text,
              user_id text,
              username text,
              screenname text,
              link_to_profile text,
              permalink text,
              language text,
              time date,
              timestamp timestamp,
              retweets int,
              likes int,
              text text );"

    print(SQL_cmd)

    conn = make_conn()
    result = fetch(conn,SQL_cmd)

    conn.close()

    return result