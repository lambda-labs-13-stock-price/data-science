import pandas as pd
import praw
from access_psycopg2 import make_conn,fetch

# thanks Mac for the Reddit credentials

REDDIT_CLIENT_ID = "VXYCrQAymaBrLQ"
REDDIT_CLIENT_SECRET = "0Wwvv9zptchx7iqweK52cvbtX4A"
REDDIT_USER_AGENT = "WSB"

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret = REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

def subreddit_query(subreddits):

    query = ""

    if isinstance(subreddits, list):
        for item in subreddits:
            query += item + '+'

    if query.endswith('+'):
        query = query[:-1]

    return query

def stream_subreddits(subreddits):

    query = subreddit_query(subreddits)
    stream = reddit.subreddit(query)



    # Mac's logic from https://github.com/lambda-labs-13-stock-price-2/reddit-scraper/blob/master/scrape.py
    # for comment in stream.stream.comments():
    #     df = pd.DataFrame({
    #         'id': [comment.id],
    #         'text': [comment.body],
    #         'time': [comment.created_utc],
    #         'subreddit_id': [comment.subreddit_id]
    #         # can add sentiment scores here, but we just want to do it raw
    #         })
    #     df.to_sql('reddit-comments', engine, if_exists='append')

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
