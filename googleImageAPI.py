import os, json
from serpapi import GoogleSearch

def getImageLink(game):
    params = {
    "api_key": "5b9c4228022e9cce8d288d0af14004cce63957b5922e2335b410631025d686b6",
    "engine": "google",
    "q": game,
    "tbm": "isch"
  }
    search = GoogleSearch(params)
    results = search.get_dict()   

    return((json.dumps(results['images_results'][0]["thumbnail"], indent=2, ensure_ascii=False)))
