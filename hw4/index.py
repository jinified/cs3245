#!/use/bin/env python3

import sys
import argparse
from collections import defaultdict, OrderedDict

from utility.util import *

''' Index files into dictornary and posting list
Expected operations: tokenize, stemmer and case folding 
'''


def generate_word_dict(filedir):
    ''' Generates dictionary of posting list
    return: dictionary and length of documents processed'''
    corpus = create_corpus_xml(filedir)
    doc_ids = get_doc_ids(filedir)
    word_dict = defaultdict(list)
    print("Generating Word Dict")
    for i in doc_ids:
        # Generates frequency distribution from processed words
        fdist = getFreqDist(preprocess(corpus.words(i)))
        # Calculates L2 Norm for term frequency in document
        tf_norm = calcL2Norm([tf(freq) for freq in fdist.values()])

        for word, freq in fdist.items():
            word_dict[word].append((i, tf(freq)/tf_norm))

    # Sort according to weight descending order
    word_dict = {term:
        ['{} {}'.format(i[0], i[1]) for i in sorted(posting, key=lambda x:x[1], reverse=True)] 
        for term, posting in word_dict.items()}
    return OrderedDict(sorted(word_dict.items())), len(doc_ids)


def index(input_path, dictionary_path, posting_path):
    ''' Optimisation 
    1. Store top K docIds'''
    word_dict, N = generate_word_dict(input_path)

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
    return parser.parse_args(args)

if __name__ == "__main__":
    result = parse_args(sys.argv[1:])
    index(result.input, result.dict, result.postings)
