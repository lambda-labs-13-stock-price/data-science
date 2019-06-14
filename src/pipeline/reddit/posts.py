from .database.tables import RedditPost, pg_utcnow
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import praw, os

TABLE = 'reddit_posts'

HOST = os.environ['PG_HOSTNAME']
PORT = os.environ['PG_PORT']
USER = os.environ['PG_USERNAME']
PASS = os.environ['PG_PASSWORD']
NAME = os.environ['PG_DBNAME']

REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']

REDDIT = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def handler(event, context):
    postgres_params = dict(
        drivername='postgres',
        username=USER,
        password=PASS,
        host=HOST,
        port=PORT,
        database=NAME
    )

    url = URL(**postgres_params).__to_string__()
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    if TABLE not in inspect(engine).get_table_names():
        raise Exception("Unable to find the table '%s' in '%s'".format(TABLE, url))

    for comment in REDDIT.subreddit('all').stream.comments():
        reddit_post = RedditPost(
            text=comment.body,
            time=comment.created_utc,
            timestamp=pg_utcnow(),
            subreddit_id=comment.subreddit_id
        )
        session.add(reddit_post)

    session.commit()
