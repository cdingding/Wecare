import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from numpy import array, matrix, linalg
# from nltk.stem.porter import PorterStemmer
from build_model import remove_punc_and_digits, LemmaTokenizer #import from build_model.py

def reconst_mse(target, left, right):
    return (array(target - left.dot(right))**2).mean()

def describe_nmf_results(document_term_mat, W, H, n_top_words = 15):
    print("Reconstruction error: %f") %(reconst_mse(document_term_mat, W, H))
    for topic_num, topic in enumerate(H):
        print("Topic %d:" % topic_num)
        print(" ".join([feature_words[i] \
                for i in topic.argsort()[:-n_top_words - 1:-1]]))

if __name__ == "__main__":
    n_features = 1000
    n_topics = 5
    # STEMMER = PorterStemmer()

    data = pd.read_csv('datacopy/history.csv')
    doc_bodies = data['comments_replies'].apply(remove_punc_and_digits)
    doc_bodies = doc_bodies.dropna() #added by ding/mia

    #vectorizer = CountVectorizer(max_features=n_features)
    vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(),max_features=n_features, stop_words='english')
    document_term_mat = vectorizer.fit_transform(doc_bodies.values)
    feature_words = vectorizer.get_feature_names()

    print("\n\n---------\nsklearn decomposition")
    nmf = NMF(n_components=n_topics)
    W_sklearn = nmf.fit_transform(document_term_mat)
    H_sklearn = nmf.components_
    describe_nmf_results(document_term_mat, W_sklearn, H_sklearn)