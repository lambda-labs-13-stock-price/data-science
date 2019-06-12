import numpy as np
import pandas as pd
from flask import Flask, abort, jsonify, request, url_for
import random
import sqlalchemy as db


app = Flask(__name__)

engine = db.create_engine('postgresql+psycopg2://HIDDENALPHABET:password@hiddenalphabet-db.ceqxyonbodui.us-east-1.rds.amazonaws.com:5432/HiddenAlphabet')
connection = engine.connect()
metadata = db.MetaData()
testtable = db.Table('reddit-comments', metadata, autoload=True, autoload_with=engine)
query = db.select([testtable])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
df = pd.DataFrame(ResultSet)
df.columns = ResultSet[0].keys()
def df_query(series, k):
    
    d = {'tsla':['tsla', 'tesla']}
    
    found = [series.str.lower().str.contains(x) for x in d[k]]
    result = df[(found[0] | found[1])]
    
    return result

@app.route('/')
def default():
   return 'API is working'

@app.route('/data')
def data():
    #result = df[['sentiment_score','time']][df['text'].str.contains(input)].to_dict()
    result = df[['sentiment_score', 'time']].tail(20).to_dict()
    return jsonify(result)

#Currently functional route for users to search
@app.route('/data/<search>')
def data_search(search):
   result2 = df[['sentiment_score','time']][df['text'].str.contains(search)].to_dict()
   return jsonify(result2)


#Route for Production
@app.route('/api', methods=['POST'])
def predict():
   input = request.get_json(force=True)
   search = input['query']
   df_final = df_query(df.text, search)
   score = df_final['sentiment_score'].mean()

   return jsonify(score=score)

if __name__ == '__main__':
    app.run()
