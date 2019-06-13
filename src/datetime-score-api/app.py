import numpy as np
import pandas as pd
from flask import Flask, abort, jsonify, request, url_for
import random
import sqlalchemy as db
from functools import reduce


app = Flask(__name__)

file = []
with open('tickers.txt','r') as inf:
    for line in inf:
        file.append(eval(line))
ticker_aliases = file[0]


@app.route('/', methods=['POST'])
def data_search(search):
   engine = db.create_engine('postgresql+psycopg2://HIDDENALPHABET:password@hiddenalphabet-db.ceqxyonbodui.us-east-1.rds.amazonaws.com:5432/HiddenAlphabet')
   connection = engine.connect()
   metadata = db.MetaData()
   testtable = db.Table('reddit-comments', metadata, autoload=True, autoload_with=engine)
   query = db.select([testtable])
   ResultProxy = connection.execute(query)
   ResultSet = ResultProxy.fetchall()
   CORPUS = pd.DataFrame(ResultSet)
   CORPUS.columns = ResultSet[0].keys()
   scores = CORPUS[['sentiment_score','time']]
   does_match_search = CORPUS['text'].str.contains(search)
   matching_scores = scores[does_match_search]
   return jsonify(matching_scores.to_dict())


if __name__ == '__main__':
    app.run()