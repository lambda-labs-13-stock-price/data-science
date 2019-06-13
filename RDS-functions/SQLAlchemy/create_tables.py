from sqlalchemy import MetaData, Table, Column, String, Integer
from utils import ENGINE, CreateTable, CreateTweetsTable

METADATA = MetaData()
METADATA.reflect(bind=ENGINE)

# useful function, will be deprecated when class object is built out and reusable.

def create_table(name, METADATA):
	'''
		Create a new table with a specified name.
		:name: Name of table (i.e. donald_trump_tweets, nancy_pelosi_tweets)
		:metadata: Specified metadata 
	'''
	tables = METADATA.tables.keys()
	if name not in tables: 
		table = CreateTable()
		table.create(engine)

# Probably will be deprecated 
def create_tweets_table(name, METADATA):
	'''
		To create initial tweets table
	'''
	tables = METADATA.tables.keys()
	if name not in tables:
		table = CreateTweetsTable()
		table.create(ENGINE)
