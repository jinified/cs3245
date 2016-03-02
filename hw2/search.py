#!/use/bin/env python3
import os
import sys
import getopt
import glob
import math

from collections import defaultdict
from collections import OrderedDict

from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from util import *

''' Computes doc_ids that matches a Boolean query'''

dictionary = {}

class Expression:
    """
    An expression is either a token or the product of several expressions connected by operators
    In the latter case, number of expressions = number of operators + 1
    hasnot indicates if there is a NOT operator in front of an expression
    """
    def __init__(self, expressions, operators, token, hasnot):
        self.expressions = expressions
        self.operators = operators
        self.token = token
        self.result = 0
        self.hasnot = hasnot

    def __repr__(self):
        return str(self.hasnot) + ' ' + \
        str(self.expressions) + ' ' + str(self.operators) + ' ' + str(self.token)

    @classmethod
    def fromexpressions(cls, expressions, operators, hasnot):
        return cls(expressions, operators, None, hasnot)

    @classmethod
    def fromtoken(cls, token, hasnot):
        return cls(None, None, token, hasnot)

def parse_query(query):
    print ('parsing: ' + query)
    elements = query.split();
    expressions = [];
    operators = [];
    # Parse tokens and operators as lists of expressions and strings of operators respectively
    # Merge elements within parentheses
    merging_parentheses = False
    having_not_operator = False
    parentheses_content = ''
    # print elements

    for element in elements:
        # print '   ' + element
        if merging_parentheses and element.endswith(')'):
            parentheses_content += element.replace(')', '')
            # Recursively parse parentheses content
            expressions.append(parse_query(parentheses_content))
            parentheses_content = ''
            having_not_operator = False
            merging_parentheses = False
        elif merging_parentheses:
            parentheses_content += element + ' '
        elif element == 'AND' or element == 'OR':
            operators.append(element)
        elif element == 'NOT':
            having_not_operator = True
        elif element.startswith('(') and not element.endswith(')'):
            merging_parentheses = True
            parentheses_content = element.replace('(', '') + ' '
        else:
            expressions.append(Expression.fromtoken(element, having_not_operator))
            having_not_operator = False
        # print '\n'.join(str(p) for p in expressions)

    return Expression.fromexpressions(expressions, operators, None)
        # query = stemmer.stem(elements[x])


def execute_query(parsed_query):
    print 'parse result:'
    print '\n'.join(str(p) for p in parsed_query.expressions)
    print parsed_query.operators
    print '---------'
    # print(dictionary[query])
    # print(get_posting_list(dictionary[query], posting_file_p))

def search():
    stemmer = PorterStemmer()
    ''' TODO remove last newline'''
    global queries_file_q, dictionary_file_d, posting_file_p, output_file_o
    with open(dictionary_file_d) as dicts:
        for i, term in enumerate(dicts):
            term = term.strip('\r\n').strip('\n')
            # print(i, term)
            dictionary[term] = i
    with open(queries_file_q) as queries:
        for query in queries:
            execute_query(parse_query(query.strip('\r\n').strip('\n')))
    
def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p posting-file -q file-of-queries"
    + " -o output-file-of-results")

queries_file_i = dictionary_file_d = posting_file_p = output_file_o = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        queries_file_q = a
    elif o == '-d':
        dictionary_file_d = a
    elif o == '-p':
        posting_file_p = a
    elif o == '-o':
        output_file_o = a
    else:
        assert False, "unhandled option"
if output_file_o == None or dictionary_file_d == None or posting_file_p == None or queries_file_q == None:
    usage()
    sys.exit(2)

if __name__ == "__main__":
    search()
