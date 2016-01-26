#!/usr/bin/env python
import math
from itertools import chain

import nltk
from  nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.probability import *

# Should we lowercase all the words 

def generate_single_ngram(n, sentence):
    """
    param n: number of gram 
    return list of 4grams as string 
    """
    return [''.join(i) for i in ngrams(list(sentence), n)]

def generate_ngram(n, sentences):
    result = [generate_single_ngram(4, i) for i in sentences]
    #flatten the list
    return list(chain.from_iterable(result))
        
def generate_fdist(ngrams):
    return FreqDist(ngrams)

def generate_MLEprob(ngrams):
    return MLEProbDist(FreqDist(ngrams))

def get_unique_list(ngrams):
    return list(set(ngrams))

def union_LM(langs):
    """
    param langs: list of ngrams 
    return vocabulary
    """
    return set().union(*langs)

def calcSmoothingConstant(ngrams, vocab):
    smooth = len(set(vocab) - set(ngrams))
    return smooth

def calcProb(ngrams, vocab):
    smooth = calcSmoothingConstant(ngrams, vocab)
    fdist = generate_fdist(ngrams)
    total_count = fdist.N() + smooth;
    return {k:math.log(v+smooth/float(total_count)) for k,v in fdist.items()}
    

def read_input(filename):
    lang_dict = {'malaysian': [], 'indonesian': [], 'tamil': [], 'other': []}
    with open(filename) as f:
        for line in f:
            sentence = line.split();
            label = sentence[0]
            content = sentence[1:]
            lang_dict[label].append(' '.join(content))
    return lang_dict

def main():
    lang_dict = read_input("input.correct.txt")
    m_ngram = generate_ngram(4, lang_dict['malaysian'])
    i_ngram = generate_ngram(4, lang_dict['indonesian'])
    t_ngram = generate_ngram(4, lang_dict['tamil'])
    vocab = union_LM([m_ngram, i_ngram, t_ngram])
    m_prob = calcProb(m_ngram, vocab)
    print(m_prob)

if __name__ == "__main__":
    main()
