from sqlalchemy.sql import text
from tables import Tweets

def all_tweets(session):
    return session.query(Tweets).all()

def tweets_between(session, start, finish):
    return session.query(Tweets).filter(start >= Tweets.time & Tweets.time <= finish)