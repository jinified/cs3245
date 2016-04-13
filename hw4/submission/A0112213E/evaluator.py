#!/usr/bin/env python3

import codecs as c
from search import search

"""
Main test suite for different queries
"""


def test_query(predicted, pos_result, neg_result):
    count = correct = unknown = 0
    sumPrecision = sumRecall = sumFMeasure = 0
    pos = neg = []

    with c.open(pos_result, encoding='utf-8') as pos_docs, c.open(neg_result, encoding='utf-8') as neg_docs:
        pos = [i.rstrip() for i in pos_docs]
        neg = [i.rstrip() for i in neg_docs]

    total_positive = len(pos)

    for patent in predicted.split():
        count += 1
        if patent in pos:
            correct += 1
        elif patent in neg:
            pass
        else:
            unknown += 1

        precision = 0.0 if count == unknown else correct / float(count - unknown)
        recall = 0.0 if count == unknown else correct / float(total_positive)
        sumPrecision += precision
        sumRecall += recall
        sumFMeasure += calc_fmeasure(precision, recall)
    return [sumPrecision / count, sumRecall / count, sumFMeasure / count]


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
    return numerator / denominator if precision > 0 and recall > 0 else 0.0

if __name__ == '__main__':
    DICT = 'dictionary.txt'
    POSTINGS = 'postings.txt'
    RESULT = './output/result{}.txt'
    QUERY = './test/q{}.xml'
    POS = './test/q{}_pos.txt'
    NEG = './test/q{}_neg.txt'

    for i in xrange(1, 5):
        predicted = search(QUERY.format(i), DICT, POSTINGS, RESULT.format(i))
        precision, recall, fmeasure = test_query(predicted, POS.format(i), NEG.format(i))
