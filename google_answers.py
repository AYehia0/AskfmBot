"""
Faster way to fetch answers from the web using google search engine API
"""
import os
import json
from googleapiclient.discovery import build

try:

    api_key = os.environ['G_ID']
    cse_key = os.environ['C_ID']
except:
    pass


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()

    # checking for valid query
    if 'items' in res.keys():
        return res['items']
    return None


def get_answer(question):
    result = google_search(question, api_key, cse_key)

    # cheking for invalid query
    if result is not None:
        return result[0]['snippet']
    else:
        return "What do you mean, i am stupid"
