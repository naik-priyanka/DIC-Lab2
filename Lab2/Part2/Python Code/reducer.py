#!/usr/bin/env python
'''reducer.py'''
import json, sys

def reducer(file_name):
    d = {}
    for line in file_name:
        line = line.strip()
        word, count = line.split(" ", 1)
        try:
            d[word] += int(count)
        except:
            d[word] = int(count)
    s = json.dumps([{'term': word, 'freq': count} for word, count in d.items()], indent = 4)
    print s

def main():
    reducer(sys.stdin)

if __name__ == "__main__":
    main()
