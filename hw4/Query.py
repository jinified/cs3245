#!/usr/bin/env python3
import codecs
import xml.etree.ElementTree as ET
from collections import defaultdict

import util
"""
Represents a query used for patent retrieval task
"""


class Query:

    def __init__(self, query_file, terms_dictionary, patent_info):
        self.terms_dictionary = self.get_terms_dictionary(terms_dictionary)
        self.patent_info = patent_info
        self.corpus_size = len(patent_info) - 1
        self.avg_doc_length = self.get_avg_doc_length(patent_info)

        self.title, self.desc = Query.parse(query_file)
        self.terms = self.get_terms()

        self.terms_dist = util.getFreqDist(self.terms)
        self.tf_weights = util.get_tf_weights(self.terms_dist)

        self.docterm_matrix = self.get_docterms_matrix()

    def __repr__(self):
        return 'Title: {}\nDesc: {}'.format(self.title, self.desc)

    def get_terms(self):
        """ Return terms separated by whitespace """
        terms = util.remove_punctuations(self.desc)
        terms = [i for i in (terms.split()[4:]) if i is not '']
        return [util.normalize_token(i) for i in util.remove_stopwords(terms) if not i.isdigit()]

    def get_tf(self, term):
        return self.terms_dist[term] if term in self.terms_dist else 0.0

    def get_avg_doc_length(self, patent_info):
        """ Extracts average document length and delete key from dictionary """
        avg_doc_length = patent_info['avg_doc_length']
        del patent_info['avg_doc_length']
        return avg_doc_length

    def get_docterms_matrix(self):
        result = defaultdict(float)
        N = self.corpus_size
        avg_doc_length = self.avg_doc_length
        total_score = 0.0
        for id, doc in self.patent_info.items():
            for term in self.terms:
                tfq = self.get_tf(term)
                tfd = doc.get_tf(term)
                df = int(self.terms_dictionary[term][0]) if term in self.terms_dictionary else 0.0
                cf = int(self.terms_dictionary[term][1]) if term in self.terms_dictionary else 0.0
                doc_length = len(doc.terms)

                '''
                result[id] += (util.bm25(tfd, df, N, doc_length, avg_doc_length) *
                               util.bm25(tfq, df, N, doc_length, avg_doc_length))

                result[id] += util.dfr(tfq, tfd, df, N, doc_length, avg_doc_length)

                '''
                result[id] += util.es(tfq, tfd, df, N, cf, doc_length, avg_doc_length)

        return result

    def get_terms_dictionary(self, terms_dictionary):
        return {k.split(',')[0]: (k.split(',')[1], k.split(',')[2]) for k in terms_dictionary.keys()}

    def get_ranked_docs(self):
        return sorted(self.docterm_matrix, key=self.docterm_matrix.get, reverse=True)

    @staticmethod
    def parse(query_file):
        """ Parses query file into respective fields """
        with codecs.open(query_file, encoding='utf-8') as xml_file:
            root = ET.parse(xml_file).getroot()
            assert root.tag == 'query'
            title = root.find('title').text.strip()
            desc = root.find('description').text.strip().replace('\n', ' ').replace('/', ' ')
            return title, desc


if __name__ == '__main__':
    TEST_QUERY = './test_resource/q1.xml'
    q1 = Query(TEST_QUERY)
