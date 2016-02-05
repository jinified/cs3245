#!/usr/bin/env python
import os
import math
from itertools import chain

import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.probability import *

''' Represents a Language Model for a selected langugage i.e malaysian'''
class LangModel:

    def __init__(self, lang_name, ngrams, vocab):
        self.lang_name = lang_name
        self.vocab = vocab
        self.ngrams = ngrams
        self.fdist = FreqDist(ngrams)
        self.total_smooth = 1
        self.total_count = self.init_total_samples()
        self.gram_from_other_LM = math.log(1.0/(self.total_count), 2)
        self.pdf = self.init_prob()
        self.matched_ngram = 0

    def init_total_samples(self):
        self.total_smooth = len(set(self.vocab) - set(self.ngrams))
        '''Calculates total number of samples after smoothing'''
        total_count = self.fdist.B()*self.total_smooth + self.fdist.N() + self.total_smooth;
        return total_count

    def init_prob(self):
        return {k:math.log((v+self.total_smooth)/float(self.total_count),2) for k,v in self.fdist.items()}

    def get_log_prob(self, target_gram):
        if target_gram in self.pdf:
            self.matched_ngram += 1
            return self.pdf[target_gram]
        elif target_gram in self.vocab:
            return self.gram_from_other_LM
        else:
            return 0

    def get_sentence_prob(self, target_grams):
        '''Reset matched ngram after each query sentence'''
        self.matched_ngram = 0
        result = self.lang_name, sum(self.get_log_prob(i) for i in target_grams)
        return result


def generate_sentence_ngram(n, sentence):
    ''' Generates ngram represented by a string for one sentence'''
    return [''.join(i) for i in ngrams(list(sentence), n)]

def generate_ngram(n, sentences):
    result = [generate_sentence_ngram(n, i) for i in sentences]
    return list(chain.from_iterable(result))
        
def generate_vocab(langs):
    '''Returns vocabulary from training data'''
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

def calc_highest_prob(sentence, LModels, n=4):
    ''' Returns language  with highest probability for the sentence'''
    target_grams = generate_sentence_ngram(n, sentence)
    prob_result = dict([lm.get_sentence_prob(target_grams) for k,lm in LModels.items()])
    predictedLabel = max(prob_result, key=prob_result.get)
    if(LModels[predictedLabel].matched_ngram  < 3):
        predictedLabel = 'other'
    return predictedLabel + " " + sentence

def process_queries(query_list, LModels, out_name, n=4):
    res = []
    for num, sentence in enumerate(query_list):
        predicted = calc_highest_prob(sentence, LModels, n)
        res.append(predicted)
    write_output(out_name, "\n".join(res))

