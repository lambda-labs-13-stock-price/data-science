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

def make_conn():
	
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name,db_user,db_host,db_pass))
    except:
        logger.error("Unexpected error: Could not connect to RDS-PostgreSQL instance")
        sys.exit()

    return conn

def fetch(conn,query):

    print('Executing Query : %s' % (query))
    result = []
    cursor = conn.cursor()
    cursor.execute(query)
    raw = cursor.fetchall()

    for line in raw:
        result.append(line)

    return result