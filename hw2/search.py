#!/use/bin/env python3
import os
import sys
import getopt
import glob
import math
import time

from collections import defaultdict
from collections import OrderedDict

from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

from util import *

''' Computes doc_ids that matches a Boolean query'''
start_time = time.time()

dictionary = {}

# 14818 is not accurate as some documents were skipped in the training set
# TOTAL_DOCUMENTS = 14818
TOTAL_DOCUMENTS = 7769

class Expression:
    """
    An expression is either a token, or the product of several expressions connected by operators
    In the latter case, number of expressions = number of operators + 1
    negated indicates if there is a NOT operator in front of an expression
    """
    def __init__(self, expressions, operators, token, negated):
        self.expressions = expressions
        self.operators = operators
        self.token = token
        self.size = 0
        self.has_result = False
        self.result = []
        self.negated = negated

    def __repr__(self):
        return str(self.negated) + ' ' + \
        str(self.expressions) + ' ' + str(self.operators) + ' ' + str(self.token)

    @classmethod
    def fromexpressions(cls, expressions, operators, negated):
        return cls(expressions, operators, None, negated)

    @classmethod
    def fromtoken(cls, token, negated):
        return cls(None, None, token, negated)      

def parse_query(query, is_query_negated = False):
    print('parsing: ' + query)
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
        if merging_parentheses and element.endswith(')'):
            parentheses_content += normalize_token(element.replace(')', ''))
            # Recursively parse parentheses content
            expressions.append(parse_query(parentheses_content, having_not_operator))
            parentheses_content = ''
            having_not_operator = False
            merging_parentheses = False
        elif merging_parentheses and (element == 'AND' or element == 'OR'):
            parentheses_content += element + ' '
        elif merging_parentheses:
            parentheses_content += normalize_token(element) + ' '
        elif element == 'AND' or element == 'OR':
            operators.append(element)
        elif element == 'NOT':
            having_not_operator = True
        elif element.startswith('(') and not element.endswith(')'):
            merging_parentheses = True
            parentheses_content = normalize_token(element.replace('(', '')) + ' '
        else:
            expressions.append(Expression.fromtoken(normalize_token(element), having_not_operator))
            having_not_operator = False

    return Expression.fromexpressions(expressions, operators, is_query_negated)
        # query = stemmer.stem(elements[x])

def intersect_postings(res1, res2):
    # print(res1)
    # print(res2)
    answer = []
    counter1 = 0
    counter2 = 0
    while counter1 < len(res1) and counter2 < len(res2):
        docID1 = int(res1[counter1][0])
        docID2 = int(res2[counter2][0])
        if docID1 == docID2:
            answer.append(str(docID1))
            counter1 += 1
            counter2 += 1
        elif docID1 < docID2:
            skip_pointer = int(res1[counter1][1])
            if (not skip_pointer == -1) and (int(res1[skip_pointer][0]) < docID2):
                # print('skip 1')
                counter1 = skip_pointer
            else:
                counter1 += 1
        else:
            skip_pointer = int(res2[counter2][1])
            if (not skip_pointer == -1) and (int(res2[skip_pointer][0]) < docID1):
                # print('skip 2')
                counter2 = skip_pointer
            else:
                counter2 += 1
    # Re-calculate skip pointers
    answer = generate_skiplist(answer)
    return answer

def union_postings(res1, res2):
    answer = []
    counter1 = 0
    counter2 = 0
    while counter1 < len(res1) and counter2 < len(res2):
        docID1 = int(res1[counter1][0])
        docID2 = int(res2[counter2][0])
        if docID1 == docID2:
            answer.append(str(docID1))
            counter1 += 1
            counter2 += 1
        elif docID1 < docID2:
            answer.append(str(docID1))
            counter1 += 1
        else:
            answer.append(str(docID2))
            counter2 += 1
    while counter1 < len(res1):
        answer.append(str(docID1))
        counter1 += 1
    while counter2 < len(res2):
        answer.append(str(docID2))
        counter2 += 1
    # Re-calculate skip pointers
    answer = generate_skiplist(answer)
    return answer

def merge_postings(res1, res2, operator):
    if operator == 'AND':
        return intersect_postings(res1, res2)
    elif operator == 'OR':
        return union_postings(res1, res2)
    else:
        print('Invalid operator')
        exit(-1)    

def merge_expressions(expression1, expression2, operator):
    '''
    Performs merge on two child expressions, 
    returns a lits of postings of docIDs of merging two expressions
    '''
    return merge_postings(search_expression(expression1), search_expression(expression2), operator)

def get_naive_operator_order(operators):
    '''returns the order of operators based on type of operator'''
    orderAND = []
    orderOR = []
    for i, operator in enumerate(operators):
        if operator == 'AND':
            orderAND.append(i)
        elif operator == 'OR':
            orderOR.append(i)
        else:
            print('Invalid operator')
            exit(-1)
    return orderAND + orderOR

def get_sized_operator_order(operators, sizes):
    '''
    Returns the order of operators based on type of operator and sizes of expressions
    List of sizes always has 1 more element than operators
    '''
    orderAND = []
    orderOR = []
    for i, operator in enumerate(operators):
        sizeEstimate = get_combined_size_estimate(sizes[i], sizes[i + 1], operator)
        if operator == 'AND':
            orderAND.append(i)
        elif operator == 'OR':
            orderOR.append(i)
        else:
            print('Invalid operator')
            exit(-1)
    sorted(orderAND, key=lambda i:sizes[i])
    sorted(orderOR, key=lambda i:sizes[i])
    return orderAND + orderOR

def get_combined_size_estimate(first_size, second_size, operator):
    '''returns the combined size of two expressions'''
    if operator == 'AND':
        return min(first_size, second_size)
    elif operator == 'OR':
        return first_size + second_size
    else:
        print('Invalid operator')
        exit(-1)

def get_size(expression):
    '''returns the size of an expression'''
    if expression.token is not None:
        # Expression is token
        if expression.token not in dictionary:
            return 0
        if expression.negated:
            return TOTAL_DOCUMENTS - int(dictionary[expression.token][1])
        else:
            return int(dictionary[expression.token][1])
    else:
        size = 0
        consumed_expressions_indices = []
        order = get_naive_operator_order(expression.operators)
        size = get_combined_size_estimate(get_size(expression.expressions[order[0]]), 
                get_size(expression.expressions[order[0] + 1]), expression.operators[order[0]])
        consumed_expressions_indices.append(order[0])
        consumed_expressions_indices.append(order[0] + 1)
        for i in order[1:]:
            if i in consumed_expressions_indices:
                # because operators AND and OR are left and right associative, we need to decide which
                # expression to be combined
                size = get_combined_size_estimate(size, get_size(expression.expressions[i + 1]),
                    expression.operators[order[i]])
                consumed_expressions_indices.append(i + 1)
            else:
                size = get_combined_size_estimate(size, get_size(expression.expressions[i]),
                    expression.operators[order[i]])
                consumed_expressions_indices.append(i)
        return size

def negate_posting(posting):
    # All postings of entire docIDs is stored at the end of postings file
    # TODO: Optimize this very inefficient way of converting between postings and skip lists
    all_postings = posting_from_skip_list(get_posting_list(len(dictionary) + 1, posting_file_p))
    # Remove duplicates
    posting = list(OrderedDict.fromkeys(posting))
    return generate_skiplist([x for x in all_postings if x not in posting])

def get_negated_posting(token):
    present_postings = posting_from_skip_list(get_posting_list(token, posting_file_p))
    return negate_posting(present_postings)

def search_expression(expression):
    '''Performs serach on an expression and returns the postings of DocIDs as a list'''
    if expression.token is not None:
        # Expression is token
        if expression.negated:
            return get_negated_posting(dictionary[expression.token][0])
        else:
            return get_posting_list(dictionary[expression.token][0], posting_file_p)
    elif len(expression.expressions) == 1:
        return search_expression(expression.expressions[0])
    else:
        sizes = [get_size(i) for i in expression.expressions]
        search_order = get_sized_operator_order(expression.operators, sizes)
        consumed_expressions_indices = []
        postings = merge_expressions(expression.expressions[search_order[0]], 
                expression.expressions[search_order[0] + 1], expression.operators[search_order[0]])
        consumed_expressions_indices.append(search_order[0])
        consumed_expressions_indices.append(search_order[0] + 1)
        for i in search_order[1:]:
            if i in consumed_expressions_indices:
                # because operators AND and OR are left and right associative, we need to decide which
                # expression to be combined
                postings = merge_postings(postings, search_expression(expression.expressions[i + 1]), 
                    expression.operators[search_order[i]])
                consumed_expressions_indices.append(i + 1)
            else:
                postings = merge_postings(postings, expression.expressions[i],
                    expression.operators[search_order[i]])
                consumed_expressions_indices.append(i)
        if expression.negated:
            return negate_posting(posting_from_skip_list(postings))
        else:
            return postings
    # print(dictionary[query])
    # print(get_posting_list(dictionary[query], posting_file_p))

def search():
    stemmer = PorterStemmer()
    global queries_file_q, dictionary_file_d, posting_file_p, output_file

    # List of posting_list in string format
    results = []
    with open(dictionary_file_d) as dicts:
        for i, term in enumerate(dicts):
            term, freq = term.strip('\r\n').strip('\n').split(' ')
            dictionary[term] = (i + 1, freq)
            # term = term.strip('\r\n').strip('\n')
            # dictionary[term] = (i + 1, 1)

    with open(queries_file_q) as queries:
        for query in queries:
            print('==============')
            expression = parse_query(query.strip('\r\n').strip('\n'))
            result = posting_from_skip_list(search_expression(expression))
            # Remove dulplicates
            result = list(OrderedDict.fromkeys(result))
            results.append(" ".join(result))
            print('result')
            print(" ".join(result))

    with open(output_file, "w") as o:
        o.write('\n'.join(results))
    
def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p posting-file -q file-of-queries"
    + " -o output-file-of-results")

queries_file_i = dictionary_file_d = posting_file_p = output_file = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'q:d:p:o:')
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
        output_file = a
    else:
        assert False, "unhandled option"
if output_file == None or dictionary_file_d == None or posting_file_p == None or queries_file_q == None:
    usage()
    sys.exit(2)

if __name__ == "__main__":
    search()
    print("--- %s seconds ---" % (time.time() - start_time))
