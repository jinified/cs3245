#!/use/bin/env python3
import os
import glob
import math
import heapq
from collections import defaultdict, OrderedDict
from itertools import islice

from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.cluster.util import cosine_distance

stemmer = PorterStemmer()   

''' Queries '''
def processQueries(queries, dictionary):
    ''' Return normalized query and weight pair '''
    queries = [normalize_token(i) for i in queries]
    queries_tf = [tf(freq) for query in queries]
    tf_norm = calcL2Norm(queries_tf)
    return [(query, queries_tf/tf_norm) for query,query_tf in zip(queries, queries_tf)] 

''' Statistics '''

def rank_docIds(query_list, k=10):
    # TODO Divide by document length for score '''
    ranked = defaultdict(int)
    
    # Ignore non-matched query
    for query in query_list:

        if query[1] > 0:
            for posting in query[2]:
                ranked[int(posting[0])] += (query[1] * posting[1])

    return sorted(ranked, key=ranked.get, reverse=True)[:k]

def getFreqDist(words):
    return FreqDist(words)

def calcL2Norm(weights):
    ''' Calculates L2 Norm for given weights '''
    return math.sqrt(sum([weight**2 for weight in weights]))

def tf_idf(N, term_freq, doc_freq):
    return tf(term_freq) * df(doc_freq)

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

def get_posting_list(index, filepath):
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
        return posting_list 
    
if __name__ == "__main__":
    pass