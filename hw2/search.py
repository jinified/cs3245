#!/use/bin/env python3
import os
import sys
import getopt
import glob
import math

from collections import defaultdict
from collections import OrderedDict

from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from util import *

''' Computes doc_ids that matches a Boolean query'''

dictionary = {}

def search():
    stemmer = PorterStemmer()
    ''' TODO remove last newline'''
    global queries_file_q, dictionary_file_d, posting_file_p, output_file_o
    with open(dictionary_file_d) as dicts:
        for i, term in enumerate(dicts):
            term = term.strip('\r\n').strip('\n')
            # print(i, term)
            dictionary[term] = i
    with open(queries_file_q) as queries:
        for query in queries:
            print (query)
            query = stemmer.stem(query.strip('\r\n').strip('\n'))
            print(dictionary[query])
            print(get_posting_list(dictionary[query], posting_file_p))


    
def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p posting-file -q file-of-queries"
    + " -o output-file-of-results")

queries_file_i = dictionary_file_d = posting_file_p = output_file_o = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        queries_file_q = a
    elif o == '-d':
        dictionary_file_d = a
    elif o == '-p':
        posting_file_p = a
    elif o == '-o':
        output_file_o = a
    else:
        assert False, "unhandled option"
if output_file_o == None or dictionary_file_d == None or posting_file_p == None or queries_file_q == None:
    usage()
    sys.exit(2)

if __name__ == "__main__":
    search()
