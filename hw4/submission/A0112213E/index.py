#!/use/bin/env python

import sys
import argparse
import codecs as c

import util
from Document import Doc

"""
Indexes given corpus

"""

PATENT_INFO_PATH = 'patent_info.txt'


def index(input_path, dictionary_path, postings_path):
    """ Saves dictionary and postings file """
    docs, terms_dictionary = Doc.get_patent_info(input_path)
    # Save patent info
    util.save_dictionary(docs, PATENT_INFO_PATH)
    write_dictionary_postings(terms_dictionary, docs, dictionary_path, postings_path)


def write_dictionary_postings(term_dictionary, docs, dictionary_path, postings_path):
    """ Write dictionary and posting pair to relevant paths """
    with c.open(dictionary_path, "w", encoding='utf-8') as d, c.open(postings_path, "w", encoding='utf-8') as p:
        dictionary, postings = get_dictionary_postings(term_dictionary, docs)
        d.write(dictionary)
        p.write(postings)


def get_dictionary_postings(terms_dictionary, docs):
    dictionary = '\n'.join('{},{},{}'.format(
        term, len(posting), sum([docs[i].get_tf(term) for i in posting])) for term, posting in terms_dictionary.items())
    postings = '\n'.join([','.join(posting) for posting in terms_dictionary.values()])
    return dictionary, postings


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Indexes files into dictionary and postings")
    parser.add_argument('-i', '--input', help='corpus location', required=True)
    parser.add_argument('-d', '--dict', help='dictionary output', default='dictionary.txt')
    parser.add_argument('-p', '--postings', help='postings output', default='postings.txt')
    return parser.parse_args(args)

if __name__ == "__main__":
    result = parse_args(sys.argv[1:])
    index(result.input, result.dict, result.postings)
