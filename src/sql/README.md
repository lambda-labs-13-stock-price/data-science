# RDS

In this repo all of the RDS related Lambda functions will reside here

- there is a repo for psycopg2 solution and SQLAlchemy solution.
- To be honest I do not know how effective it is for me to have created solutions with different methods, but time will tell. 

**DISCLAIMER**
- Files in this repository are not intended to be tested locally or on any test environment, just with AWS tools and services.
- Unless specified, there are `os.environ` environment variables that need to be set before usage. 

## FAQ (sort of):

- [What is an Amazon Relational Database Service?](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [How to connect to a DB instance running PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html)
- [Working with Read Replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.Replication.ReadReplicas.html)
- [Cheatsheet of tasks for DBA](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#CHAP_PostgreSQL.CommonTasks)
- [More DBA tasks](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.html)
