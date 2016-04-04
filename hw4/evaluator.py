#!/usr/bin/env python3

import codecs

from search import primary_search

import constants as c

"""
Main test suite for different queries
"""


def test_query(index):
    result = result_to_list(primary_search(c.QUERY % index, c.DICTIONARY, c.POSTINGS, c.OUTPUT))
    expected = file_to_list(c.POSITIVE_RESULT % index)
    return evaluate_search_result(expected, result % index)


def result_to_list(result):
    """
    Returns:
        newline separated result to a list
    """
    return result.split('\n')


def file_to_list(filedir):
    """
    Returns:
        newline separated string in file to a list
    """
    expected = []
    with codecs.open(filedir, encoding='utf-8') as expected_file:
        expected = [i.strip('\r\n').strip('\n') for i in expected_file]
    return expected


def evaluate_search_result(expected, predicted):
    """
        Returns:
            dictionary    f2-measure, precision and recall
    """
    tp = len(set(expected).intersection(predicted))
    recall = tp / len(expected)
    precision = tp / len(predicted)
    f2measure = calc_fmeasure(precision, recall)
    return {'f2': f2measure, 'p': precision, 'r': recall}


def calc_fmeasure(precision, recall, weight=2):
    """
    Calculates f2-measure by default
        Arguments:
            weight    determines weightage of precision and recall. Higher favors recall more
        Returns:
            f-measure    calculated f-measure 
    """
    numerator = (1 + weight**2) * (precision * recall)
    denominator = (weight**2 * precision) + recall
    # Prevent division by zero
    return numerator / (denominator + 0.0001)

if __name__ == '__main__':
    for i in range(1, 3):
        print(test_query(i))
