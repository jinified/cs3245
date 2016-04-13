#!/bin/bash

# Indexing
# echo Indexing
# python index.py -i ./data/original_patsnap -d dictionary.txt -p postings.txt &&

# Running search
python evaluator.py &&

# Evaluating
./eval.pl -q ./output/result1.txt ./test/q1-qrels.txt && 
./eval.pl -q ./output/result2.txt ./test/q2-qrels.txt && 
./eval.pl -q ./output/result3.txt ./test/q3-qrels.txt && 
./eval.pl -q ./output/result4.txt ./test/q4-qrels.txt 
