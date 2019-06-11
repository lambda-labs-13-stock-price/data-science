from sqlalchemy import create_engine, Column, Integer, JSON, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_utils import db_host

engine = create_engine(db_host)
Base = declarative_base
Session = sessionmaker(bind=engine)

class Post(Base):
    """
    Post
    """
    __tablename__ = 'reddit_comments'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    time = Column(String)
    subreddit_id = Column(String)

class PostJSON(Base):

    __tablename__ = 'reddit_comments_json'

    id = Column(Integer, primary_key=True)
    data = Column(JSON)

Base.metadata.create_all(engine)

