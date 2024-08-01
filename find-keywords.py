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
ELSEVIER_API_KEY = os.getenv('ELSEVIER_API_KEY')

# TODO: not sure if acm has an api, maybe use crossref instead
def query_acm(query):
    if not ACM_API_KEY:
        return None
    url = f"https://api.acm.org/v1/articles?query={query}&apikey={ACM_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print("ACM API request failed with status code {}".format(response.status_code))
        return None
    data = response.json()
    keywords = []
    for paper in data['articles']:
        if 'keywords' in paper:
            for keyword in paper['keywords']:
                keywords.append(keyword)
    return keywords

def query_ieee(query):
    if not IEEE_API_KEY:
        return None
    url = f"https://ieeexploreapi.ieee.org/api/v1/search/articles?apikey={IEEE_API_KEY}&querytext={query}"
    response = requests.get(url)
    if response.status_code != 200:
        print("IEEE API request failed with status code {}".format(response.status_code))
        return None
    data = response.json()
    keywords = []
    for paper in data['articles']:
        if 'keywords' in paper:
            for keyword_group in paper['keywords']:
                for keyword in keyword_group['keyword']:
                    keywords.append(keyword)
    return keywords


def query_elsevier(query):
    url = "https://api.elsevier.com/content/search/scopus"
    params = {
        "query": query,
        "apiKey": ELSEVIER_API_KEY,
        "count": 10,  # Number of results to fetch
        "view": "complete",  # required to get authkeywords
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Elsevier API request failed with status code {}".format(response.status_code))
        return None

    keywords = []
    for entry in response.json()['search-results']['entry']:
        if 'authkeywords' in entry:
            keywords.extend(entry['authkeywords'].split("|"))

    return list(set(keywords))  # Remove duplicates


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
        acm_keywords = query_acm(args.search_string)
        if acm_keywords:
            all_keywords += acm_keywords

    if IEEE_API_KEY:
        ieee_keywords = query_ieee(args.search_string)
        if ieee_keywords:
            all_keywords += ieee_keywords

    if ELSEVIER_API_KEY:
        elsevier_keywords = query_elsevier(args.search_string)
        if elsevier_keywords:
            all_keywords += elsevier_keywords

    # Rank keywords
    ranked_keywords = rank_keywords(all_keywords)

    # Print ranked keywords
    for keyword, count in ranked_keywords:
        print(f"{keyword}: {count}")

