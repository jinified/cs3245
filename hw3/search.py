#!/use/bin/env python3

import sys
import time
import argparse
import logging

from util import *

''' Computes doc_ids that matches a free text query'''

# Setup environment
start_time = time.time()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search(queries_path, dictionary_path, posting_path, output_path, k):
    dictionary = {}
    results = []

    with open(dictionary_path) as dicts:
        for i, term in enumerate(dicts):
            term, freq = term.split(' ')
            dictionary[term] = (i + 1, freq)

    with open(queries_path) as queries:
        for query in queries:
            result = get_score(handleQuery(query.rstrip('\r\n').rstrip('\n').strip(' '), 
                               dictionary, posting_path, k))
            results.append(' '.join(str(x) for x in result))

    with open(output_path, "w") as o:
        o.write('\n'.join(results))
        o.write('\n')


def handleQuery(query, dictionary, posting_path, k):
    ''' Returns (term, normalized tf-idf, posting_list) '''
    query = [normalize_token(i) for i in query.split(' ')]
    fdist = getFreqDist(query)
    weights = [tf(freq) * float(dictionary.get(word, (0, 0))[1]) for word, freq in fdist.items()]
    weights_norm = calcL2Norm(weights)
    # Prevent division by zero error
    return [(q, w/(weights_norm+0.000001), [] if q not in dictionary else get_posting_list(dictionary[q][0], posting_path, k))
        for q, w in zip(query, weights)]


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Indexes files into dictionary and postings")
    parser.add_argument('-q', '--queries', required=True, help='list of user queries')
    parser.add_argument('-d', '--dict', required=True, help='dictionary output', default='dictionary.txt')
    parser.add_argument('-p', '--postings', required=True, help='postings output', default='postings.txt')
    parser.add_argument('-o', '--output', help='result of running query', default='output.txt')
    parser.add_argument('-k', '--kDocs', help='number of matching docIds', default=10)
    # Optinal flags
    # parser.add_argument('--s', help='remove stop words', action='store_true')
    return parser.parse_args(args)

if __name__ == "__main__":
    result = parse_args(sys.argv[1:])
    search(result.queries, result.dict, result.postings, result.output, result.kDocs)
    print("--- %s seconds ---" % (time.time() - start_time))
