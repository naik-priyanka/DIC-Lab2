#!/usr/bin/env python
'''mapper.py'''
import os, json, sys
import pandas as pd
from nltk.tokenize import word_tokenize
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import string

emoticons_str = r"""
    (?:
    [:=;] # Eyes
    [oO\-]? # Nose (optional)
    [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
             emoticons_str,
             r'<[^>]+>', # HTML tags
             r'(?:@[\w_]+)', # @-mentions
             r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
             r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
             r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
             r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
             r'(?:[\w_]+)', # other words
             r'(?:\S)' # anything else
             ]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

def read_input(file):
    tweets = []
    for line in file:
        tweets.append(json.loads(line))
    return tweets

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    filtered_tokens = [token for token in tokens if token not in stop]
    return filtered_tokens

def mapper(tweets):
    tokens = []
    terms_only = []
    d = []
    for tweet in tweets[:5]:
        tokens.extend(preprocess(tweet['text']))
        # Count terms only (no hashtags, no mentions)
        terms_only.extend([term for term in preprocess(tweet['text']) if not term.startswith(('#', '@'))])
    for term in terms_only:
        d.append((term.encode('utf-8'), 1))
    return d

def main():
    tweets = read_input(sys.stdin)
    d = mapper(tweets)
    for t in d:
        print t[0], t[1]

if __name__ == "__main__":
    main()
