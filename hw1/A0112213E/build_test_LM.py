#!/usr/bin/python
import re
from nltk.util import ngrams
import nltk
import sys
import getopt
from utility import *

def build_LM(in_file):
    """
    build language models for each label
    """
    print('building training data from {}'.format(in_file))
    # Stores list of sentences for each language label
    training_dict = read_train_input("input.train.txt")

    print('generating ngrams model for each language')
    lang_ngram = {k: generate_ngram(6, v) for k,v in training_dict.items()}
    # Generates total vocabulary covered by the training data
    vocab = generate_vocab(lang_ngram.values())
    # Generate probabilistic LM from all the ngrams
    LM = {k: LangModel(k, v, vocab) for k,v in lang_ngram.items()}
    return LM
    
def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print('reading test input')
    test_input = read_test_input(in_file)

    print('generating output')
    process_queries(test_input, LM, out_file, 6)

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

if __name__ == "__main__":
    LM = build_LM(input_file_b)
    test_LM(input_file_t, output_file, LM)

