#!/use/bin/env python3

import sys
import os
import math
import nltk
import pickle
import re

from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')
stopwords = set(nltk.corpus.stopwords.words('english'))


''' Statistics '''


def getFreqDist(words):
    return FreqDist(words)


def calcL2Norm(weights):
    ''' Calculates L2 Norm for given weights '''
    return math.sqrt(sum([weight**2 for weight in weights]))

''' Ranking function '''


def es(tfq, tfd, df, N, cf, doc_length, avg_doc_length):
    """ Calculates Evolutionary Learned Scheme score(q, D) for a document
        Arguments:
            tfq             query's term frequency
            tfd             document's term frequency
            N               number of documents in collection
            cf              number of terms in document
    """
    # idf function
    w3 = math.sqrt((float(cf**3) * N) / df**4)
    doc_ratio = doc_length / float(avg_doc_length)
    numerator = tfd * w3 * tfq
    denominator = tfd + 0.45 * doc_ratio
    return numerator / denominator


def piv(tfq, tfd, df, N, doc_length, avg_doc_length, s=0.2):
    """ Calculates Pivoted normalization method score(q, D) for a document
        Arguments:
            tfq             query's term frequency
            tfd             document's term frequency
            N               number of documents in collection
            s               normalization factor
    """
    # idf function
    w2 = math.log10((N + 1) / df)
    doc_ratio = doc_length / float(avg_doc_length)
    numerator = 1 + math.log10(1 + math.log10(tfd)) * w2 * tfq
    denominator = (1 - s) + s * doc_ratio
    return numerator / denominator


def dfr(tfq, tfd, df, N, doc_length, avg_doc_length):
    """ Calculates Divergence From Randomness score(q, D) for a document
        Arguments:
            tfq             query's term frequency
            tfd             document's term frequency
            N               number of documents in collection
    """
    doc_ratio = doc_length / float(avg_doc_length)
    numerator = tfd * math.log10(1 + doc_ratio) * math.log10((N + 1) / (df + 0.5)) * tfq
    denominator = 1 + tfd * math.log10(1 + doc_ratio)
    return numerator / denominator


def bm25(tf, df, N, doc_length, avg_doc_length, k1=1.2, k3=1.2, b=0.75):
    """ Calculates Okapi BM25 score(q, D) for a document. Can be used for query and
    document
        Arguments:
            N               documents size
            k1              controls doc frequency scaling
            k3              controls term frequency scaling
            b               controls document length scaling
    """
    numerator = idf(N, df) * (k1 + 1) * tf
    denominator = k1((1 - b) + b * (doc_length / float(avg_doc_length))) + tf
    return numerator / denominator


def tf_idf(N, term_freq, doc_freq):
    return tf(term_freq) * idf(doc_freq)


def tf(term_freq):
    ''' Calculates term frequency with log base 10'''
    assert term_freq > 0
    return 1 + math.log10(term_freq)


def idf(N, df):
    ''' Calculates inverse document frequency with log base 10'''
    assert df > 0
    return math.log10(N/df)


def get_tf_weights(term_dist):
    """ Calculates tf weight for each term given term distribution """
    tf_weights = {term: tf(freq) for term, freq in term_dist.items()}
    tf_norm = float(calcL2Norm(tf_weights.values()))
    return {term: weight / tf_norm for term, weight in tf_weights.items()}

''' Preprocess '''


def remove_stopwords(terms):
    return [i for i in terms if i not in stopwords and len(i) > 2]


def remove_punctuations(term):
    return re.sub('[^a-zA-Z0-9-]+', ' ', term)


def normalize_token(token, stemming=True, casefolding=True):
    # Remove any symbols except for hyphen
    token = token.strip('-+')

    if stemming:
        token = stemmer.stem(token)
    return token.lower() if casefolding else token

''' Input/Output '''


def get_files_path(directory):
    """ Return absolute file paths in a directory """
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def save_dictionary(dictionary, output_path):
    with open(output_path, 'w') as o:
        pickle.dump(dictionary, o)


def load_dictionary(input_path):
    with open(input_path, 'r') as i:
        return pickle.load(i)


def safeprint(msg):
        print msg.encode(sys.getdefaultencoding(), 'replace')

if __name__ == '__main__':
    print(remove_punctuations('thi/ths;'))
