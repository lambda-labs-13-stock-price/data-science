from sqlalchemy.sql import text
from tables import Tweets, RedditComments

def all_tweets(session):
    return session.query(Tweets).all()

def tweets_between(session, start, finish):
    return session.query(Tweets).filter(start >= Tweets.time & Tweets.time <= finish)

def all_reddit_comments(session):
    return session.query(RedditComments).all()

def reddit_comments_between(session, start, finish):
    return session.query(RedditComments).filter(start >= RedditComments.time & RedditComments.time <= finish)

