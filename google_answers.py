"""
Faster way to fetch answers from the web using google search engine API
"""
import os
import json
from googleapiclient.discovery import build

api_key = os.environ['G_ID']
cse_key = os.environ['C_ID']

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def get_answer(question)
    result = google_search(question, api_key, cse_key)

    return result[1]['snippet']
