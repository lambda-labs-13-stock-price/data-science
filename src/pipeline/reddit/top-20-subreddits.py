import praw
import os
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

HOST = os.environ['PG_HOSTNAME']
PORT = os.environ['PG_PORT']
USER = os.environ['PG_USERNAME']
PASS = os.environ['PG_PASSWORD']
TABLE = 'reddit_posts'
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
REDDIT_USER_AGENT = os.environ['REDDIT_USER_AGENT']

REDDIT = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

'''
    Goal :
    Crawl N subscribers
    for top 20 subreddits
    ETL job that executes everyday/beginning of the day
    Schedule to use requests api on http://redditlist.com/all
    create a table for top 20 subreddits
    write job that gets top N posts with all comments insert into table
    from /r/all
    job executes every hour ish
    exclude meme subreddits and NSFW jk lmao love NSFW
'''

def handler(event, context):
    postgres_params = dict(
        drivername='postgres',
        username=USER,
        password=PASS,
        host=HOST,
        port=PORT
    )
    url = URL(**postgres_params).__to_string__()
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    subreddits = [lolol]
    query = "+".join(subreddits)
        stream = reddit.subreddit(query)

        # Mac's logic from https://github.com/lambda-labs-13-stock-price-2/reddit-scraper/blob/master/scrape.py
        for comment in stream.stream.comments():
            df = pd.DataFrame({
                'id': [comment.id],
                'text': [comment.body],
                'time': [comment.created_utc],
                'subreddit_id': [comment.subreddit_id]
                # can add sentiment scores here, but we just want to do it raw
                })
            df.to_sql('reddit_comments', engine, if_exists='append')