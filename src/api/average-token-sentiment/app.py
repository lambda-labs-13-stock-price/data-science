from flask import Flask, jsonify, request
from functools import reduce
import sqlalchemy as db
import pandas as pd
import json
import os

TICKERS_TO_COMPANY = json.loads(open('tickers.json').read())

PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']
PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    url = 'postgresql://'+PG_USER+':'+PG_PASS+'@'+PG_HOST+':'+PG_PORT+'/HiddenAlphabet'
    engine = db.create_engine(url)
    connection = engine.connect()
    metadata = db.MetaData()
    comments = db.Table('reddit-comments', metadata, autoload=True, autoload_with=engine)

    query = db.select([comments])
    cursor = connection.execute(query)
    rows = cursor.fetchall()

    corpus = pd.DataFrame(rows)
    corpus.columns = rows[0].keys()
    json = request.get_json(force=True)

    ticker = json['query']

    lowercase = corpus['text'].str.lower()
    contains_name_masks = [lowercase.str.contains(company) for company in TICKERS_TO_COMPANY[ticker]]
    any_company_alias = reduce(lambda agg, curr: agg | curr, contains_name_masks)

    matching = corpus[any_company_alias]
    average_score = matching['sentiment_score'].mean()

    return jsonify(score=average_score)

if __name__ == '__main__':
    app.run()
