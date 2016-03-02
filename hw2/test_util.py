#!/usr/bin/env python3
import os

import util

''' Test resources '''
postings  = os.path.join(os.path.dirname(__file__), 'test/postings.txt')
dictionary  = os.path.join(os.path.dirname(__file__), 'test/dictionary.txt')

def test_get_posting_list():
    assert util.get_posting_list(1, postings)[:2] == [('1','3'),('2','-1')]
