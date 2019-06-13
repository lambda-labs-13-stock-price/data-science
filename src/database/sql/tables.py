from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

# per https://docs.sqlalchemy.org/en/13/core/compiler.html#utc-timestamp-function
# Given that SQLAlchemy does not by default support conversion to UTC timestamps from
# Unix timestamps, the following class and function thereafter implement a means to
# automatically convert from the latter to the former.
class utcnow(expression.FunctionElement):
    type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element,compiler,**kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class Tweets(Base):
    '''
    CreateTable : no default name, must inherit Base object and specify a name
    with __tablename__.
    inheritable object that can instantiate different tweets tables
    if we need to a) create new tables with different names,
    or automate table creation in the future.
    '''
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
    timestamp = Column(DateTime(timezone=True), server_default=pg_utcnow())
    retweets = Column(Integer)
    likes = Column(Integer)
    text = Column(String)