lexicon = dict(zip(pd.read_csv('Downloads/vader_lexicon.csv', encoding='cp437', header=None)[[0, 1]].values.T[0], pd.read_csv('Downloads/vader_lexicon.csv', encoding='cp437', header=None)[[0, 1]].values.T[1]))
s = Sentiment(lexicon=lexicon)
