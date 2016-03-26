#!/use/bin/env python3

import sys
import unicodedata
import os
import math
import nltk
from collections import OrderedDict
from itertools import islice

from nltk.probability import FreqDist
from nltk.stem.porter import PorterStemmer
from nltk.corpus import XMLCorpusReader
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from parser import *

''' Global '''

stemmer = PorterStemmer()
stopwords = set(nltk.corpus.stopwords.words('english')) 
# Punctuations for unicode string
exclude = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))

''' Statistics '''


def get_score(query_list):
    ranked = OrderedDict()

    # Ignore non-matched query
    for query in query_list:
        if query[1] > 0:

            for posting in query[2]:
                # Removes extension
                key = posting[0].split('.')[0]
                if key not in ranked:
                    ranked[key] = 0
                ranked[key] += (query[1] * posting[1])
    
    res = sorted(ranked, key=ranked.get, reverse=True)
    return res[:50]


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


def preprocess(words):
    ''' Returns a words with stopwords removal, stemmed and case-folded'''
    return [normalize_token(i) for i in words if i not in stopwords]


def normalize_token(token):
    ''' Normalization steps include:
    stemming, case-folding, removing punctuations '''
    return stemmer.stem(token.lower()).translate(exclude)

''' Input/Output '''


def get_doc_ids(filedir):
    # Removes any file extension
    return os.listdir(filedir)


def list_to_string(target_list, delimiter=','):
    ''' Generates delimiter i.e ',' separated string'''
    return delimiter.join(target_list)


def write_to_file(filepath, content):
    with open(filepath, 'w') as output:
        output.write(content)

''' Posting list '''


def get_posting_list(index, filepath):
    '''Retrieves a posting list given a file handle
    format: "docId1 tf_norm1", "docId2 tf_norm2" ... '''
    with open(filepath) as postings:
        posting_list = []

        try:
            posting_list = next(islice(postings, index - 1, None)).rstrip('\n').rstrip('\r\n').split(',')
            return [[i.split(' ')[0], float(i.split(' ')[1])] for i in posting_list]
        except StopIteration:
            print("Encounters end of iterator")
        return posting_list

''' Documents representation ''' 


def create_corpus(filedir):
    ''' Creates a corpus based on files that matches the regex in file directory'''
    return PlaintextCorpusReader(filedir, ".*")


def create_corpus_xml(filedir):
    ''' Creates a corpus based on XML files that matches the regex in file directory'''
    return XMLCorpusReader(filedir, ".*")


def create_corpus_xml2(filedir):
    ''' Creates a corpus based on XML files using XML parser ''' 
    return {i: parse_xml(filedir + '/' + i) for i in get_doc_ids(filedir)}

''' UNIT TESTS '''

DATA_DIR = '../data/original_patsnap'
DOC1 = 'EP0049154B2.xml'


def test_create_corpus_xml():
    corpus = create_corpus_xml(DATA_DIR)
    assert len(corpus.fileids()) == len(get_doc_ids(DATA_DIR))
