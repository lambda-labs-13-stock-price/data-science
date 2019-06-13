from flask import Flask, abort, jsonify, request, url_for
import sqlalchemy as db
import pandas as pd
import numpy as np
import random
import json

app = Flask(__name__)

TICKERS = json.loads(open('tickers.json').read())

@app.route('/', methods=['POST'])
def main(search):
   engine = db.create_engine('postgresql+psycopg2://HIDDENALPHABET:password@hiddenalphabet-db.ceqxyonbodui.us-east-1.rds.amazonaws.com:5432/HiddenAlphabet')
   connection = engine.connect()

   metadata = db.MetaData()
   comments = db.Table('reddit-comments', metadata, autoload=True, autoload_with=engine)
   query = db.select([comments])
   cursor = connection.execute(query)
   rows = cursor.fetchall()

   corpus = pd.DataFrame(rows)
   corpus.columns = rows[0].keys()

   scores = CORPUS[['sentiment_score','time']]
   does_match_search = CORPUS['text'].str.contains(search)
   matching_scores = scores[does_match_search]

   return jsonify(matching_scores.to_dict())

if __name__ == '__main__':
    app.run()
