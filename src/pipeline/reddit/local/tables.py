from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy import Column, Numeric, Integer, String, DateTime

Base = declarative_base()

class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element,compiler,**kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class RedditPost(Base):
    __tablename__ = 'reddit_posts'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    time = Column(Numeric)
    subreddit_id = Column(String)
    score = Column(Integer)