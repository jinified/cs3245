#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import xml.etree.ElementTree as ET
from collections import defaultdict

import util
"""
Represents a patent document

Extracted fields: Patent Number, Title, Abstract, All IPC/UPC, Family Members, Cites
"""


class Doc:

    # Fields that will be used for processing
    FIELDS = ['patent number', 'title', 'abstract', 'all ipc', 'all upc', 'family members', 'cites']

    def __init__(self, doc_file):
        # Raw fields extracted from XML file
        self.fields = self.parse(doc_file)

        # Initialization of fields
        self.id = self.fields['patent number']
        self.abstract = self.get_abstract()
        self.terms = self.get_terms()
        self.cites = self.get_cited_patents()
        self.cited_by = []
        self.related = self.get_related_patents()
        self.ipc = self.get_IPC_groups()
        self.upc = self.get_UPC_groups()

        self.terms_dist = util.getFreqDist(self.terms)
        self.tf_weights = util.get_tf_weights(self.terms_dist)

    def __repr__(self):
        return "Id: {}\nTitle: {}\nIPC: {}\nUPC: {}".format(
            self.fields['patent number'], self.fields['title'],
            self.ipc, self.upc)

    def parse(self, doc_file):
        """ Parses doc file into respective fields """
        with codecs.open(doc_file, encoding='utf-8') as xml_file:
            root = ET.parse(xml_file).getroot()
            assert root.tag == 'doc'
            return {e.get('name').lower(): e.text.strip() for e in root if Doc.is_valid_field(e)}

    def get_terms(self):
        """ Return list of normalized terms extracted from title and abstract field """
        # self.fields['title'] = util.remove_punctuations(self.fields['title'])
        terms = util.remove_punctuations(self.fields['title']).split() + self.abstract
        normalized_terms = [util.normalize_token(term) for term in util.remove_stopwords(terms)]
        return normalized_terms

    def get_abstract(self):
        if 'abstract' not in self.fields:
            return []
        else:
            abstract = util.remove_punctuations(self.fields['abstract'])
            return [i for i in abstract.split() if not i.isdigit()]

    def get_cited_patents(self):
        return [i.strip() for i in self.fields['cites'].split('|')] if 'cites' in self.fields else []

    def get_related_patents(self):
        return [i.strip() for i in self.fields['family members'].split('|')] if 'family members' in self.fields else []

    def get_UPC_groups(self):
        """ Returns UPC groups registered by the patent """
        return [i.split('/')[0].strip() for i in self.fields['all upc'].split('|')] if 'all upc' in self.fields else []

    def get_IPC_groups(self):
        """ Returns IPC groups registered by the patent """
        return [i.split('/')[0].strip() for i in self.fields['all ipc'].split('|')] if 'all ipc' in self.fields else []

    def get_doc_length(self):
        return len(self.terms)

    def get_tf(self, term):
        return self.terms_dist[term] if term in self.terms_dist else 0.0

    @staticmethod
    def is_valid_field(element):
        return element.get('name').lower() in Doc.FIELDS

    @staticmethod
    def citation_analysis(docs):
        """ Assign list of patents that cited a particular patents """
        for doc in docs.values():
            if doc.cites:
                for patent in doc.cites:
                    if patent in docs:
                        docs[patent].cited_by.append(doc.id)

    @staticmethod
    def get_patent_info(input_path):
        """ Return dictionary of patent number as key and doc object as value
        Also add aditional information such as citation analysis
            Returns:
                patent_info        dictionary of docs
                term_dictionary    dictionary of terms and postings
        """
        docs = {}
        term_dictionary = defaultdict(list)

        for doc_file in util.get_files_path(input_path):
            doc = Doc(doc_file)
            docs[doc.id] = doc
            for term in doc.terms:
                term_dictionary[term].append(doc.id)

        Doc.citation_analysis(docs)
        docs['avg_doc_length'] = sum([i.get_doc_length() for i in docs.values()]) / len(docs)
        return docs, term_dictionary


if __name__ == '__main__':
    input_path = '../data/original_patsnap'
    doc1 = Doc('./test_resource/doc3.xml')
    print(doc1.ipc)
