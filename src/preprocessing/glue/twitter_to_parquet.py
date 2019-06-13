import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

glueContext = GlueContext(SparkContext.getOrCreate())
DB = "RDS_tweets"
TABLE = "tweets"
input_dir = "http://s3.us-west-2.amazonaws.com/hiddenalphabet/datasets"
output_dir = "http://s3.us-west-2.amazonaws.com/hiddenalphabet/transformed_datasets"

tweets_dyf = glueContext.create_dynamic_frame.from_catalog(database=DB, table_name=TABLE)
glueContext.write_dynamic_frame.from_options(frame=tweets_dyf, connection_type="s3",
                                             connection_options={"path": output_dir},
                                             format="parquet")