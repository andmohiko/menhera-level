import pickle

from sklearn.ensemble import RandomForestClassifier
from gensim.models import KeyedVectors


def load_models():
    PATH = 'models/'
    # word_embedding_model = KeyedVectors.load(PATH + 'ja-crawl-fasttext-300d-1M')
    # stopwords
    with open(PATH + 'stopwords.pickle', 'rb') as f:
        stopwords = pickle.load(f)
    # word_vector_dict
    with open(PATH + 'word_vector_dict.pickle', 'rb') as f:
        word_vector_dict = pickle.load(f)
    # gbdt model
    with open(PATH + 'rfc.pickle', 'rb') as f:
        rfc = pickle.load(f)
    return stopwords, word_vector_dict, rfc