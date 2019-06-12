import psycopg2
'''
	Creating a master file in python with strings stored variables
	that contain prebuilt SQL queries.
	In addition to that there will also be a function wrapper that will be written
	in inspiration of the SQL query
'''

create_tweets_table = 
       		"""
       		CREATE TABLE IF NOT EXISTS tweets (
                     id int primary key,
                     tweet_id text,
                     user_id text,
                     username text,
                     screenname text,
                     link_to_profile text,
                     permalink text,
                     language text,
                     time date,
                     timestamp timestamp,
                     retweets int,
                     likes int,
                     text text );
                     """

select_all_from_table = 
			"""
                     SELECT * FROM tweets
                     """

select_by_daterange = 
			"""
                     SELECT * FROM tweets
                     WHERE time
                     BETWEEN (insert time boundary here)
                     AND (insert time boundary here)
                     """