#!/use/bin/env python3

import sys
import time
import argparse
import logging
import codecs

from utility.parser import parse_xml
from utility import util

"""
Searches corpus given query in XML format and return list of patent file names
that matches the query
"""

# Setup environment
start_time = time.time()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def primary_search(queries_path, dictionary_path, posting_path, output_path):
    """ Searches dictionary and postings for patents that matched the query
        Returns:
            result      patent filenames separated by newline
    """
    dictionary = {}

    with codecs.open(dictionary_path, encoding='utf-8') as dicts:
        for i, term in enumerate(dicts):
            term, freq = term.split(' ')
            dictionary[term] = (i + 1, freq)

    result = '\n'.join(util.get_score(handleQuery(queries_path, dictionary, posting_path)))

    with open(output_path, "w") as o:
        o.write(result)
        o.write('\n')

    return result


def handleQuery(query_path, dictionary, posting_path):
    ''' Returns (term, normalized tf-idf, posting_list) '''
    words = parse_xml(query_path)['description']
    query = util.preprocess(words)
    fdist = util.getFreqDist(query)
    weights = [util.tf(freq) * float(dictionary.get(word, (0, 0))[1]) for word, freq in fdist.items()]
    weights_norm = util.calcL2Norm(weights)
    # Prevent division by zero error
    return [(q, w/(weights_norm+0.000001),
            [] if q not in dictionary else util.get_posting_list(dictionary[q][0], posting_path))
            for q, w in zip(query, weights)]


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Indexes files into dictionary and postings")
    parser.add_argument('-q', '--queries', required=True, help='list of user queries')
    parser.add_argument('-d', '--dict', required=True, help='dictionary output', default='dictionary.txt')
    parser.add_argument('-p', '--postings', required=True, help='postings output', default='postings.txt')
    parser.add_argument('-o', '--output', help='result of running query', default='output.txt')
    # Optinal flags
    # parser.add_argument('--s', help='remove stop words', action='store_true')
    return parser.parse_args(args)

if __name__ == "__main__":
    result = parse_args(sys.argv[1:])
    primary_search(result.queries, result.dict, result.postings, result.output)
    print("--- %s seconds ---" % (time.time() - start_time))
