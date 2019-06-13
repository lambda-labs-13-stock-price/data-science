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

#Route for Production
@app.route('/', methods=['POST'])
def predict():
   engine = db.create_engine('postgresql+psycopg2://HIDDENALPHABET:password@hiddenalphabet-db.ceqxyonbodui.us-east-1.rds.amazonaws.com:5432/HiddenAlphabet')
   connection = engine.connect()
   metadata = db.MetaData()
   testtable = db.Table('reddit-comments', metadata, autoload=True, autoload_with=engine)
   query = db.select([testtable])
   ResultProxy = connection.execute(query)
   ResultSet = ResultProxy.fetchall()
   CORPUS = pd.DataFrame(ResultSet)
   CORPUS.columns = ResultSet[0].keys()
   json = request.get_json(force=True)
   ticker = json['query']      

   lowercase = CORPUS['text'].str.lower()
   masks = [lowercase.str.contains(alias) for alias in ticker_aliases[ticker]]
   contains_any_alias = reduce(lambda agg, curr: agg | curr, masks)
   matching_text = CORPUS[contains_any_alias]
   average_score = matching_text['sentiment_score'].mean()

   return jsonify(score=average_score)

if __name__ == '__main__':
    app.run()
