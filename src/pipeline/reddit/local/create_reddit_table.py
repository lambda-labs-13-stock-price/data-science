from sqlalchemy import create_engine, MetaData, Table, Numeric, Column, Integer, String, DateTime
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from dotenv import load_dotenv
import praw, os

load_dotenv()

TABLE = "reddit_posts"
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

postgres_params = dict(
        drivername="postgres",
        username=USER,
        password=PASS,
        host=HOST,
        port=PORT,
        database=NAME
)

class UTC(expression.FunctionElement):
    type = DateTime()

@compiles(UTC, 'postgresql')
def pg_unix_to_utc(element,compiler,**kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

url = URL(**postgres_params)
engine = create_engine(url,echo = True)
meta = MetaData()

posts = Table(TABLE, meta,
    Column('id', Integer, primary_key=True),
    Column('text', String),
    Column('time', Numeric),
    Column('subreddit_id', String),
    Column('score', Integer)
)

meta.create_all(engine)