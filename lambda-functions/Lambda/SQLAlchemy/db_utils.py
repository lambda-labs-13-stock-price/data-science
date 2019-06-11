from subprocess import call

# on EC2 instance with AWS CLI configured for my user
# db_host = call("aws rds describe-db-instances | jq -r '.DBInstances[]|select(.DBInstanceIdentifier=='rds-reddit-data').Endpoint|.Address'", shell=True)
# else use :
db_host = "postgresql://hiddenalphabet:hiddenalphabet@rds-reddit-data.cwnallhzqgag.us-west-2.rds.amazonaws.com:5432/hiddenalphabet_reddit_data"
db_port = 5432
db_name = "hiddenalphabet_reddit_data"
db_user = "hiddenalphabet"
db_pass = "hiddenalphabet"
db_table = "reddit-comments"