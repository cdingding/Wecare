
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import cPickle as pickle
import pandas as pd
from itertools import *
from nltk import word_tokenize
from nltk.tokenize import word_tokenize as tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def remove_punc_and_digits(x):
    x = str(x).decode('utf-8')
    for c in string.punctuation + string.digits:
        x = x.replace(c,'')
    return x

def build_model(filename):
    df = pd.read_csv(filename,low_memory=False)
    vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), stop_words = 'english')
    df['comments_replies'] = df['comments_replies'].apply(remove_punc_and_digits)
    df['comments_replies'] = df['comments_replies'].fillna('')
    voc = df['comments_replies']
    X = vectorizer.fit_transform(voc)
    y = df['target']
    model = MultinomialNB().fit(X,y)
    return vectorizer, model

if __name__ == '__main__':
    vectorizer, model = build_model('data/allfilesfinal55.csv')
    with open('data/vectorizer.pkl', 'w') as f:
        pickle.dump(vectorizer, f)
    with open('data/model.pkl', 'w') as f:
        pickle.dump(model, f)