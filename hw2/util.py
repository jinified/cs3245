#!/use/bin/env python3
import os
import glob

from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

''' Index files into dictornary and posting list
Expected operations: tokenize, stemmer and case folding 
'''

stemmer = PorterStemmer()   

def create_corpus(filedir):
    ''' Creates a corpus based on files that matches the regex in file directory'''
    return PlaintextCorpusReader(filedir, ".*")

def get_doc_ids(filedir):
    return sorted(os.listdir(filedir), key=lambda x: int(x))

def normalize_token(token):
    return stemmer.stem(token.lower())

def get_posting_list(index, filepath):
    '''Retrieves a posting list given a file handle'''
    with open(filepath) as postings:
        return postings[index]
    
if __name__ == "__main__":
    pass
