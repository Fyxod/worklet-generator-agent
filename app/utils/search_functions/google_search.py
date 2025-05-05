import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

# 4 api keys - 400 requests per day after which it'll fall back to duckduckgo search
api_keys = [
    os.getenv("GOOGLE_API_KEY3"),
    os.getenv("GOOGLE_API_KEY4"),
    os.getenv("GOOGLE_API_KEY2"),
    os.getenv("GOOGLE_API_KEY1"),
]

search_engine_ids = [
    os.getenv("SEARCH_ENGINE_ID3"),
    os.getenv("SEARCH_ENGINE_ID4"),
    os.getenv("SEARCH_ENGINE_ID2"),
    os.getenv("SEARCH_ENGINE_ID1"),
]

api_key_ref = os.getenv("GOOGLE_API_KEY_ref")
search_engine_id_ref = os.getenv("SEARCH_ENGINE_ID_ref")


url = 'https://www.googleapis.com/customsearch/v1'

def google_search(query, max_results=10):
    arr = []

    for api_key, cx in zip(api_keys, search_engine_ids):
        if not api_key or not cx:
            continue

        params = {
            'q': query,
            'key': api_key,
            'cx': cx,
            "num": max_results,
        }

        try:
            response = requests.get(url, params=params, timeout=6)
            response.raise_for_status()
            results = response.json()

            if 'items' in results and results['items']:
                for item in results['items']:
                    arr.append({
                        "title": item.get('title'),
                        "link": item.get('link'),
                        "body": item.get('snippet'),
                        "query": query,
                    })

                with open('search_results.json', 'w') as f:
                    json.dump(results['items'], f, indent=4)

                return True, arr

        except requests.exceptions.RequestException as e:
            print(f"API key ending with {api_key[-4:]} with cx {cx} failed: {e}")

    # If all API keys fail, return an empty list
    return False, arr

def google_search_references(query, max_results=10):
    arr = []
    
    params = {
        'q': query,
        'key': api_key_ref,
        'cx': search_engine_id_ref,
        "num": max_results,
    }
    
    try:

        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        if 'items' in results and results['items']:
            for item in results['items']:
                arr.append({
                    "Title": item.get('title'),
                    "Link": item.get('link'),
                    "Description": item.get('snippet'),
                    "Tag": "google",
                })

            return True, arr
        
    except requests.exceptions.RequestException as e:
        return False, arr