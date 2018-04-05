#!/usr/bin/env python
'''reducer-co.py'''
import json, sys
from collections import defaultdict
import operator

def reducer(file_name):
    co_oc = defaultdict(lambda : defaultdict(int))
    for line in file_name:
        line = line.strip()
        word, co_word, count = line.split(" ", 2)
        co_oc[word][co_word] += int(count)
    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in co_oc:
        t1_max_terms = sorted(co_oc[t1].items(), key=operator.itemgetter(1), reverse=True)[:10]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    for t in terms_max[:10]:
        print '{} {} {}'.format(t[0][0], t[0][1], t[1])

def main():
    reducer(sys.stdin)

if __name__ == "__main__":
    main()
