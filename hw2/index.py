#!/use/bin/env python3
import sys
import getopt

from nltk.tokenize import sent_tokenize

''' Index files into dictornary and posting list
Expected operations: tokenize, stemmer and case folding 
'''

def usage():
    print "usage: " + sys.argv[0] + " -i training-input-file -d output-dictionary-file -p output-posting-file"

input_file_i = dictionary_file_d = posting_file_p = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        input_file_i = a
    elif o == '-d':
        dictionary_file_d = a
    elif o == '-p':
        posting_file_p = a
    else:
        assert False, "unhandled option"
if input_file_i == None or dictionary_file_d == None or posting_file_p == None:
    usage()
    sys.exit(2)

if __name__ == "__main__":
    pass

