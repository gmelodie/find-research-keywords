#!/usr/bin/env python3

import requests
import argparse
import os
from dotenv import load_dotenv
from collections import Counter
import json

# ACM_API_KEY
# IEEE_API_KEY
load_dotenv()
ACM_API_KEY = os.getenv('ACM_API_KEY')
IEEE_API_KEY = os.getenv('IEEE_API_KEY')

# TODO: not sure if acm has an api, maybe use crossref instead
def query_acm(query):
    if not ACM_API_KEY:
        return None
    url = f"https://api.acm.org/v1/articles?query={query}&apikey={ACM_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

def query_ieee(query):
    if not IEEE_API_KEY:
        return None
    url = f"https://ieeexploreapi.ieee.org/api/v1/search/articles?apikey={IEEE_API_KEY}&querytext={query}"
    response = requests.get(url)
    data = response.json()
    return data

def extract_keywords_acm(data):
    keywords = []
    for paper in data['articles']:
        if 'keywords' in paper:
            for keyword in paper['keywords']
                keywords.append(keyword)
    return keywords

def extract_keywords_ieee(data):
    keywords = []
    for paper in data['articles']:
        if 'keywords' in paper:
            for keyword_group in paper['keywords']:
                for keyword in keyword_group['keyword']:
                    keywords.append(keyword)
    return keywords

def rank_keywords(keywords):
    counter = Counter(keywords)
    ranked_keywords = counter.most_common()
    return ranked_keywords


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='find-keywords.py',
                    description='Find keywords related to a search on IEEE Xplore and ACM Digital Library')
    parser.add_argument('search_string')

    args = parser.parse_args()

    all_keywords = []

    if ACM_API_KEY:
        acm_data = query_acm(args.search_string)
        acm_keywords = extract_keywords_acm(acm_data)
        all_keywords += acm_keywords

    if IEEE_API_KEY:
        ieee_data = query_ieee(args.search_string)
        ieee_keywords = extract_keywords_ieee(ieee_data)
        all_keywords += ieee_keywords

    # Rank keywords
    ranked_keywords = rank_keywords(all_keywords)

    # Print ranked keywords
    for keyword, count in ranked_keywords:
        print(f"{keyword}: {count}")

