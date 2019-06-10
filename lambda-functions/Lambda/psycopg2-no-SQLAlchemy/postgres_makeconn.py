import sys
import logging
import psycopg2
from access_psycopg2 import make_conn, fetch

# Lambda function logic for accessing the PostgreSQL DB in RDS
# Select all data from table

def lambda_handler(event, context):
    SQL_cmd = "SELECT COUNT(\*) FROM reddit-comments"
    print(SQL_cmd)

    conn = make_conn()
    result = fetch(conn,SQL_cmd)

    conn.close()

    return result