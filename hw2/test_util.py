#!/usr/bin/env python3
import os

import util

''' Test resources '''
postings  = os.path.join(os.path.dirname(__file__), 'test/postings.txt')
dictionary  = os.path.join(os.path.dirname(__file__), 'test/dictionary.txt')

def test_get_posting_list():
    assert util.get_posting_list(1, postings) == ['1','2','3','4','5','6','6','7']
