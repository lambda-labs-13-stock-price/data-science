# Prerequisites

- PostgreSQL Database created
- Reddit API credentials
- Python 3.7 installed
- Dependencies installed from `requierements.txt`

# Getting Started

Set environment variables in a `.env` file

```python
export PG_HOSTNAME=
export PG_PORT=
export PG_USERNAME=
export PG_PASSWORD=
exoirt PG_DBNAME=
export REDDIT_CLIENT_ID=
export REDDIT_CLIENT_SECRET=
export REDDIT_USER_AGENT=
```

And that's it, all that's left to do is create the `reddit_posts` table with:

`$ python create_reddit_table.py`

Which will create a table called `reddit_posts` in your PostgreSQL database with the powerful ORM SQLAlchemy

Now if we want to stream Reddit Data into our database we execute with:

`$ python execute.py`

By default this script will terminate after 25 minutes, which is configurable in `execute.py` by changing the integer value in the `func_timeout` function here:

```python
try:
    start_handler = func_timeout(1500, handler, args=())
except FunctionTimedOut:
    print('Streaming terminated')
```

