#!/usr/bin/env python
'''mapper-news-co.py'''
import os, json, sys
import pandas as pd
from nltk.tokenize import word_tokenize
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
from collections import defaultdict

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
    articles = []
    for line in file:
        articles.append(json.loads(line))
    return articles

def parse_articles(articles):
    news = []
    if len(articles) >= 1:
        for article in articles["response"]["docs"]:
            snippet = article["snippet"] if "snippet" in article.keys() else ""
            news.append(snippet)
    return news

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    filtered_tokens = [token for token in tokens if token not in stop]
    return filtered_tokens

def mapper(news):
    tokens = []
    com = defaultdict(lambda : defaultdict(int))
    for new in news:
        tokens.extend(preprocess(new))
    # Build co-occurrence matrix
    for i in range(len(tokens)-1):
        for j in range(i+1, len(tokens)):
            w1, w2 = sorted([tokens[i].encode('utf-8'), tokens[j].encode('utf-8')])
            if w1 != w2:
                com[w1][w2] += 1
    return com

def main():
    articles = read_input(sys.stdin)
    news = parse_articles(articles[0])
    com = mapper(news)
    for k,v in com.items():
        for key,val in v.items():
            t = (k, (key, val))
            print '{} {} {}'.format(t[0], t[1][0], t[1][1])

if __name__ == "__main__":
    main()
