#!/use/bin/env python3
import os
import math
from collections import OrderedDict
from itertools import islice

from nltk.probability import FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

stemmer = PorterStemmer()

''' Statistics '''


def get_score(query_list, k=10):
    ranked = OrderedDict()

    # Ignore non-matched query
    for query in query_list:
        if query[1] > 0:

            for posting in query[2]:
                key = int(posting[0])
                if key not in ranked:
                    ranked[key] = 0
                ranked[int(posting[0])] += (query[1] * posting[1])

    res = sorted(ranked, key=ranked.get, reverse=True)[:k]
    return res


def getFreqDist(words):
    return FreqDist(words)


def calcL2Norm(weights):
    ''' Calculates L2 Norm for given weights '''
    return math.sqrt(sum([weight**2 for weight in weights]))


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

''' Preprocess '''


def normalize_token(token):
    # Converts unicode string to regular string
    return str(stemmer.stem(token.lower()))

''' Input/Output '''


def get_doc_ids(filedir):
    return sorted(os.listdir(filedir), key=lambda x: int(x))


def create_corpus(filedir):
    ''' Creates a corpus based on files that matches the regex in file directory'''
    return PlaintextCorpusReader(filedir, ".*")


def list_to_string(target_list, delimiter=','):
    ''' Generates delimiter i.e ',' separated string'''
    return delimiter.join(target_list)


def write_to_file(filepath, content):
    with open(filepath, 'w') as output:
        output.write(content)

''' Posting list '''


def get_posting_list(index, filepath, k):
    '''Retrieves a posting list given a file handle
    format: "docId1 tf_norm1", "docId2 tf_norm2" ... 
    k: upper limit of docIds returned'''
    with open(filepath) as postings:
        posting_list = []

        try:
            posting_list = next(islice(postings, index - 1, None)).rstrip('\n').rstrip('\r\n').split(',')
            return [[float(j) for j in i.split(' ')] for i in posting_list]
        except StopIteration:
            print("Encounters end of iterator")
        return posting_list[:k]

if __name__ == "__main__":
    pass
