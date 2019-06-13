from flask import Flask, jsonify, request
import sqlalchemy as db
import pandas as pd
import random
import json
import os

app = Flask(__name__)

PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']
PG_HOST = os.environ['PG_HOST']
PG_PORT = os.environ['PG_PORT']

@app.route('/', methods=['POST'])
def main():
    req = request.get_json()
    search = req['search']

    url = 'postgresql://'+PG_USER+':'+PG_PASS+'@'+PG_HOST+':'+PG_PORT+'/HiddenAlphabet'
    engine = db.create_engine(url)
    connection = engine.connect()

   corpus = pd.DataFrame(rows)
   corpus.columns = rows[0].keys()

   scores = CORPUS[['sentiment_score','time']]
   does_match_search = CORPUS['text'].str.contains(search)
   matching_scores = scores[does_match_search]

   return jsonify(matching_scores.to_dict())

if __name__ == '__main__':
    app.run()
