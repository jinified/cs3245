#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import codecs
from itertools import islice

import util
from Query import Query


"""
Performs a patent search on given list of XML queries
Returns: list of patent number that are relevant
"""

PATENT_INFO_PATH = 'patent_info.txt'

patent_info = {}
dictionary = {}


def search(queries_path, dictionary_path, postings_path, output_path):
    """ Searches dictionary and postings for patents that matches the queries """
    global patent_info, dictionary
    dictionary = read_dictionary(dictionary_path)
    patent_info = util.load_dictionary(PATENT_INFO_PATH)
    query = Query(queries_path, dictionary, patent_info)
    result = ' '.join(query.get_ranked_docs())
    with codecs.open(output_path, 'w', encoding='utf-8') as o:
        o.write(result)


def read_posting_list(index, postings_path):
    """ Retrieves a posting list given a file handle """
    with codecs.open(postings_path, 'r', encoding='utf-8') as postings:
        try:
            return next(islice(postings, index - 1, None)).decode('utf-8').rstrip('\n').rstrip('\r\n').split(',')
        except StopIteration:
            print("Encounters end of iterator")
        return []


def read_dictionary(dictionary_path):
    """ Returns stored dictionary from the given path where key = (term, doc freq, corpus freq) """
    dictionary = {}
    with codecs.open(dictionary_path, 'r', encoding='utf-8') as d:
        dictionary = {j.rstrip('\n'): i + 1 for i, j in enumerate(d)}
    return dictionary


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Retrieves relevant patents for given queries")
    parser.add_argument('-q', '--queries', required=True, help='list of user queries')
    parser.add_argument('-d', '--dict', required=True, help='dictionary output', default='dictionary.txt')
    parser.add_argument('-p', '--postings', required=True, help='postings output', default='postings.txt')
    parser.add_argument('-o', '--output', help='result of running query', default='output.txt')
    # Optinal flags
    # parser.add_argument('--s', help='remove stop words', action='store_true')
    return parser.parse_args(args)

if __name__ == "__main__":
    result = parse_args(sys.argv[1:])
    search(result.queries, result.dict, result.postings, result.output)
