#!/usr/bin/env python
import os
import math
from itertools import chain

import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.probability import *

# Should we lowercase all the words 

class LangModel:

    def __init__(self, lang_name, ngrams, vocab):
        self.lang_name = lang_name
        self.vocab = vocab
        self.ngrams = ngrams
        self.fdist = FreqDist(ngrams)
        self.total_smooth = 1
        self.total_count = self.init_total_samples()
        self.gram_from_other_LM = math.log(1.0/(self.total_count), 2)
        self.pdf = self.initProb()

    def init_total_samples(self):
        self.total_smooth = len(set(self.vocab) - set(self.ngrams))
        # Calculates total number of samples after smoothing
        total_count = self.fdist.B()*self.total_smooth + self.fdist.N() + self.total_smooth;
        return total_count

    def initProb(self):
        # Number of ngrams not in current LM
        return {k:math.log((v+self.total_smooth)/float(self.total_count),2) for k,v in self.fdist.items()}

    def get_log_prob(self, target_gram):
        if target_gram in self.pdf:
            return self.pdf[target_gram]
        elif target_gram in self.vocab:
            return self.gram_from_other_LM
        else:
            # gram does not match with vocab
            return 0

    def get_sentence_prob(self, target_grams):
        result = self.lang_name, sum(self.get_log_prob(i) for i in target_grams)
        return result



''' Statistics '''

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
        
def generate_vocab(langs):
    """
    param langs: list of ngrams 
    return vocabulary
    """
    return set().union(*langs)

''' Input/Output '''
def read_train_input(filename):
    lang_dict = {'malaysian': [], 'indonesian': [], 'tamil': []}
    with open(filename) as f:
        for line in f:
            sentence = line.split();
            label = sentence[0]
            content = sentence[1:]
            if label in lang_dict:
                lang_dict[label].append(' '.join(content))
    return lang_dict

def read_test_input(filename):
    test = []
    with open(filename) as f:
        for line in f:
            test.append(line.strip(os.linesep)) 
    return test

def write_output(out_name, output):
    with open(out_name, "w") as f:
        f.write(output)

''' Calculation '''

def calcHighestProb(sentence, LModels):
    target_grams = generate_single_ngram(4, sentence)
    # Converts to dictionary 
    prob_result = dict([lm.get_sentence_prob(target_grams) for k,lm in LModels.items()])
    predictedLabel = max(prob_result, key=prob_result.get)
    if(prob_result[predictedLabel] == 0):
        predictedLabel = 'other'
    return predictedLabel + " " + sentence

def processQueries(query_list, LModels, out_name):
    res = []
    for num, sentence in enumerate(query_list):
        predicted = calcHighestProb(sentence, LModels)
        res.append(predicted)
    write_output(out_name, "\n".join(res))


def main():
    # reading input 
    lang_dict = read_train_input("input.train.txt")
    query_list = read_test_input("input.test.txt")

    # generate ngrams
    lang_ngram = {k: generate_ngram(4, v) for k,v in lang_dict.items()}

    # generate total vocab of the three LMs
    vocab = generate_vocab(lang_ngram.values())

    LModels = {k: LangModel(k, v, vocab) for k,v in lang_ngram.items()}
    prediction = processQueries(query_list, LModels, "output.txt")

if __name__ == "__main__":
    main()
