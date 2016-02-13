#!/use/bin/env python3
import os
import sys
import getopt
import glob
import math
from collections import defaultdict

from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

''' Index files into dictornary and posting list
Expected operations: tokenize, stemmer and case folding 
'''

def create_corpus(filedir):
    return PlaintextCorpusReader(filedir, ".*")

def get_doc_ids(filedir):
    return sorted(os.listdir(filedir), key=lambda x: int(x))


def preprocess_words(word_list, stemmer):
    '''
    Return: stemmed and case folded words
    '''
    return [stemmer.stem(i.lower()) for i in word_list]

def generate_word_dict(filedir):
    ''' Generates dictionary of posting list'''
    stemmer = PorterStemmer()
    corpus = create_corpus(filedir)
    doc_ids = get_doc_ids(filedir)
    word_dict = defaultdict(list)
    print("Generating Word Dict")
    for i in doc_ids:
        words = preprocess_words(corpus.words(i), stemmer)
        
        for word in words:
            word_dict[word].append(i)
    return word_dict

def generate_skiplist(posting_list):
    skip_len = math.floor(math.sqrt(len(posting_list)))
    return [i for i in posting_list[::int(skip_len)]]

def index():
    ''' TODO remove last newline'''
    global input_file_i, dictionary_file_d, posting_file_p
    word_dict = generate_word_dict(input_file_i)
    with open(dictionary_file_d, "wu") as d, open(posting_file_p, "w") as p:
        print("Writing to files")
        for k, v in word_dict.items():
            d.write(k + "\n")
            p.write(",".join(v) + "\n")
    
def usage():
    print "usage: " + sys.argv[0] + " -i training-input-file -d output-dictionary-file -p output-posting-file"

input_file_i = dictionary_file_d = posting_file_p = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        input_file_i = a
    elif o == '-d':
        dictionary_file_d = a
    elif o == '-p':
        posting_file_p = a
    else:
        assert False, "unhandled option"
if input_file_i == None or dictionary_file_d == None or posting_file_p == None:
    usage()
    sys.exit(2)

if __name__ == "__main__":
    ls = [1,2,3,4,5,6,7,8,9]
    skip = generate_skiplist(ls)
    print(skip)
