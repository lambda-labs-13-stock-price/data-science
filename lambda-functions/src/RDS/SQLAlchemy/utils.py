import os
import logging
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import func, expression
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, DateTime

# Global variables
postgres_db = {
	'drivername':'postgres',
	'username': os.environ['PG_USERNAME'],
	'password': os.environ['PG_PASSWORD'],
	'host': os.environ['PG_HOST'],
	'port': 5432
	}

DB_URI = URL(**postgres_db)
ENGINE = create_engine(DB_URI)

Base = declarative_base()

# For PostgreSQL UTC timestamp custom function

class utcnow(expression.FunctionElement):
	type = DateTime()

@compiles(utcnow, 'postgresql')
def pg_utcnow(element,compiler,**kw):
	return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

class CreateTable(object):
	'''
	CreateTable : no default name, must inherit Base object and specify a name
	with __tablename__.
	inheritable object that can instantiate different tweets tables
	if we need to a) create new tables with different names,
	or automate table creation in the future.
	'''
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

class CreateTweetsTable(CreateTable, Base):
	__tablename__ = 'tweets'

