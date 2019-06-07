import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from sqlalchemy import create_engine
nltk.download('vader_lexicon')

engine = create_engine(
    'postgresql://HIDDENALPHABET:password@hiddenalphabet-db.ceqxyonbodui.us-east-1.rds.amazonaws.com:5432/HiddenAlphabet')


REDDIT_CLIENT_ID = "VXYCrQAymaBrLQ"
REDDIT_CLIENT_SECRET = "0Wwvv9zptchx7iqweK52cvbtX4A"
REDDIT_USER_AGENT = "WSB"

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
	
