#!/usr/bin/env python3

from search import search
from utility.util import *

''' TESTS '''
OUT = 'out'
DICT = 'dictionary.txt'
POSTINGS = 'postings.txt'
QUERY = './test/q%d.xml'
POSITIVE = './test/q%d_pos.txt'
NEGATIVE = './test/q%d_neg.txt'
DATA_DIR = './data/original_patsnap'


def test_query1():
    result = set(search(QUERY % 1, DICT, POSTINGS, OUT))
    expected = POSITIVE % 1 
    print(len(set(expected).intersection(result)))

if __name__ == '__main__':
    test_query1()
