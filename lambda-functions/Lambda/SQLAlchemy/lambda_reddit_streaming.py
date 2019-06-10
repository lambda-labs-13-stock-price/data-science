import pandas as pd
import praw
from sqlalchemy import create_engine
from db_utils import *

engine = create_engine(db_host)

REDDIT_CLIENT_ID = "VXYCrQAymaBrLQ"
REDDIT_CLIENT_SECRET = "0Wwvv9zptchx7iqweK52cvbtX4A"
REDDIT_USER_AGENT = "WSB"

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

class TWICE(object):

    def __init__(self, subreddits):

        self.subreddits = subreddits

    def subreddit_query(self, subreddits):

        query = ""

        if isinstance(self.subreddits, list):
            for item in self.subreddits:
                query += item + '+'

        if query.endswith('+'):
            query = query[:-1]

        return query

    def stream_subreddits(self):

        query = self.subreddit_query(self.subreddits)
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
