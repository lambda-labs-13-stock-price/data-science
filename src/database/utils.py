from sqlalchemy import inspect

def does_table_exist(table, engine):
	'''
	Inspect database to check whether or not a table exists.
	:name: String , name of table
	'''
	return True if table in inspect(engine).get_table_names() else False