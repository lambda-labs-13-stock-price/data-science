import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from sqlalchemy import create_engine
nltk.download('vader_lexicon')

engine = create_engine(
    'my_engine')


REDDIT_CLIENT_ID = "xyz"
REDDIT_CLIENT_SECRET = "abc"
REDDIT_USER_AGENT = "abc"

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret = REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

reddit_financials = reddit.subreddit(
        'wallstreetbets+investing+stocks+options+SecurityAnalysis+RobinHood+tradevol+thewallstreet')

for comment in reddit_financials.stream.comments():
	df = pd.DataFrame({'id': [comment.id], 'text': [comment.body],
                       'time': [comment.created_utc], 'subreddit_id': [comment.subreddit_id],
                       'sentiment_score': [sid.polarity_scores(comment.body)['compound']]})
	df.to_sql('reddit-comments', engine, if_exists='append')
	
