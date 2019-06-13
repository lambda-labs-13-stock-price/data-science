import os
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, DateTime
from utils import DB_URI, ENGINE, CreateTable, CreateTweetsTable
from create_tables import create_table, create_tweets_table

# logic for RDS related stuff goes here
# can't wait to get started.

