import psycopg2
from subprocess import call

# as the name implies, access the RDS database with pyscopg2 without the need of an ORM like SQLAlchemy
# DBInstanceIdentifier can be found by running the command after the ` in your shell
# this is a dependency file of our lambda function postgres_makeconn.py

db_host = call("aws rds describe-db-instances | jq -r '.DBInstances[]|select(.DBInstanceIdentifier=='rds-reddit-data').Endpoint|.Address'", shell=True)
db_port = 5432
db_name = "hiddenalphabet_reddit_data"
db_user = "hiddenalphabet"
db_pass = "hiddenalphabet"
db_table = "reddit-comments"

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name,db_user,db_host,db_pass))
    except:
        print('Unable to connect to Database.')

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

# Lambda function logic for accessing the PostgreSQL DB in RDS

def lambda_handler(event, context):
    '''
        Lambda function to Create a NEW Table for new Subreddit Querys
        This might be inefficient
    '''

    query_cmd = ""
    print('Query Command : ', query_cmd)

    conn = make_conn()
    result = fetch(conn, query_cmd)
    conn.close()