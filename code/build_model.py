# Today leanred to use ctrl_tab to switch files,
# cmd + tab to toggle and switch applications,
# cmd + down_arrow to open a file

# import numpy as np
# import matplotlib.pyplot as plt
# import re
# import unidecode
# from sklearn.decomposition import NMF
# import datetime
# from utils import tokenize
# from nltk.tokenize import word_tokenize as tokenize  #backup and replaced for above tokenize
# from nltk.stem.snowball import SnowballStemmer
# import pickle as pkl
# from nltk.tokenize import word_tokenize
# from pyspark.mllib.clustering import KMeans
# from collections import Counter
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer

import cPickle as pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from itertools import *
import string
from sklearn.naive_bayes import MultinomialNB
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))

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
    df = pd.read_csv(filename)
    vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), stop_words = 'english')
    df['comments_replies'] = df['comments_replies'].apply(remove_punc_and_digits)
    voc = df['comments_replies']
    # voc_cleaner = cleaner(voc)
    X = vectorizer.fit_transform(voc)
    df['SubReddit_Name']='Fitness'
    y = df['SubReddit_Name']
    model = MultinomialNB().fit(X,y)
    return vectorizer, model

if __name__ == '__main__':
    vectorizer, model = build_model('dataall/allfiles1.csv')
    with open('data/vectorizer.pkl', 'w') as f:
        pickle.dump(vectorizer, f)
    with open('data/model.pkl', 'w') as f:
        pickle.dump(model, f)

