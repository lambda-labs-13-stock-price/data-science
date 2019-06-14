import praw
import os
import time
import threading
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from tables import RedditPost, utcnow
from func_timeout import func_timeout, FunctionTimedOut

load_dotenv()

HOST = os.environ['PG_HOSTNAME']
PORT = os.environ['PG_PORT']
USER = os.environ['PG_USERNAME']
PASS = os.environ['PG_PASSWORD']
NAME = os.environ['PG_DBNAME']
TABLE = 'reddit_posts'
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']

REDDIT = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# for lambda function pass these args : (event, context)
def handler():
    postgres_params = dict(
        drivername='postgres',
        username=USER,
        password=PASS,
        host=HOST,
        port=PORT,
        database=NAME
    )
    url = URL(**postgres_params)
    print('>>> engine url created')
    engine = create_engine(url)
    print('>>> engine instantiated')
    Session = sessionmaker(bind=engine)
    print('>>> engine binded to sessionmaker')
    session = Session()
    print('>>> Session instantiated')

    # could add custom sleep here?
    # or how would we execute every hour?
    # check below for a really janky way of terminating
    print('>>> Streaming is starting')
    count = 0
    for comment in REDDIT.subreddit('all').stream.comments():
        reddit_post = RedditPost(
            text=comment.body,
            time=comment.created_utc,
            subreddit_id=comment.subreddit_id,
            score=comment.score
        )
        session.add(reddit_post)
        N = 500
        count+=1
        if count % N == 0:
            print('>>> {} New Reddit posts have been added'.format(count))
            print('>>> Committing rows to table: ', TABLE)
            session.commit()

try:
    start_handler = func_timeout(1500, handler, args=())
except FunctionTimedOut:
    print('Streaming terminated')




