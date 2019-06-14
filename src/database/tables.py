from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

# Per https://docs.sqlalchemy.org/en/13/core/compiler.html#utc-timestamp-function,
# SQLAlchemy does not, by default, support conversion to UTC timestamps from Unix
# timestamps. The `UTC` class, and `pg_unix_to_utc` function thereafter, implement a
# means of automatically converting from Unix to UTC at insert time.
class UTC(expression.FunctionElement):
    type = DateTime()

@compiles(UTC, 'postgresql')
def pg_unix_to_utc(element,compiler,**kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String)
    user_id = Column(String)
    username = Column(String)
    screenname = Column(String)
    link_to_profile = Column(String, key='profile_link')
    permalink = Column(String, key='link')
    language = Column(String)
    time = Column(DateTime)
    timestamp = Column(DateTime(timezone=True), server_default=pg_unix_to_utc())
    retweets = Column(Integer)
    likes = Column(Integer)
    text = Column(String)

class RedditComments(Base):
    __tablename__ = 'reddit_comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    time = Column(DateTime)
    timestamp = Column(DateTime(timezone=True), server_default=pg_unix_to_utc())
    subreddit_id = Column(String)
