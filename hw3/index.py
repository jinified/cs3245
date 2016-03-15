#!/use/bin/env python3

import os
import sys
import argparse
import math
from collections import defaultdict, OrderedDict

import nltk
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from util import *

''' Index files into dictornary and posting list
Expected operations: tokenize, stemmer and case folding 
'''

''' Globals ''' 
stopwords = set(nltk.corpus.stopwords.words('english'))

def generate_word_dict(filedir, remove_stopwords):
    ''' Generates dictionary of posting list
    return: dictionary and length of documents processed'''
    corpus = create_corpus(filedir)
    doc_ids = get_doc_ids(filedir)
    word_dict = defaultdict(list)
    print("Generating Word Dict")
    for i in doc_ids:
        words = [normalize_token(j) for j in corpus.words(i)]
        # Remove stopwords if specified
        if remove_stopwords: 
            words = [word for word in words if word not in stopwords]
        fdist = getFreqDist(words)
        # Calculates L2 Norm for term frequency in document
        tf_norm = calcL2Norm([tf(freq) for freq in fdist.values()])

        for word, freq in fdist.items():
            word_dict[word].append((i, tf(freq)/tf_norm))

    # Sort according to weight descending order
    word_dict = {term:
        ['{} {}'.format(i[0], i[1]) for i in sorted(posting, key=lambda x:x[1], reverse=True)] 
        for term, posting in word_dict.items()}
    return OrderedDict(sorted(word_dict.items())), len(doc_ids)

def index(input_path, dictionary_path, posting_path, remove_stopwords=False):
    ''' Optimisation 
    1. Store top K docIds'''
    word_dict, N = generate_word_dict(input_path, remove_stopwords)

    with open(dictionary_path, "w") as d, open(posting_path, "w") as p:
        print("Writing to files")
        for k, v in word_dict.items():
            d.write("{} {}\n".format(k, idf(N, len(v))))
            p.write(','.join(v) + "\n")
    
def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Indexes files into dictionary and postings")
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-d', '--dict', help='dictionary output', default='dictionary.txt')
    parser.add_argument('-p', '--postings', help='postings output', default='postings.txt')
    # Optinal flags
    parser.add_argument('--s', help='remove stop words', action='store_true')
    return parser.parse_args(args)

if __name__ == "__main__":
    result = parse_args(sys.argv[1:])
    index(result.input, result.dict, result.postings, result.s)
