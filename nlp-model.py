import re
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


class PreprocessText(object):
    """
    Sentiment relevant text properties. 
    """
    
    def __init__(self, text):
        
        self.text = text
        self.clean_text = self._clean_text()
        
    def _clean_text(self):
        
        wordz = self.text.split()
        
        lemmatizer = WordNetLemmatizer()
        words = []
        for word in wordz:
            words.append(lemmatizer.lemmatize(word))
        
        return words

class Sentiment(object):
    """
    Sentiment Analyzer
    """
    
    
    def __init__(self, lexicon):
        
        self.lexicon = lexicon
        
    def score(self, text):
        
        words = PreprocessText(text).clean_text
        
        sentiments = []
        for word in words:
            try:
                lexicon[word]
                sentiments.append(lexicon[word])
            except:
                sentiments.append(0)
                
        return sum(sentiments)
    
    
