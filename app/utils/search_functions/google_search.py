import requests
import os
import json

api_keys = [
    os.getenv("GOOGLE_API_KEY1"),
    os.getenv("GOOGLE_API_KEY2"),
]

search_engine_ids = [
    os.getenv("SEARCH_ENGINE_ID1"),
    os.getenv("SEARCH_ENGINE_ID2"),
]

url = 'https://www.googleapis.com/customsearch/v1'

def google_search(query, max_results=5):
    arr = []

    for api_key, cx in zip(api_keys, search_engine_ids):
        if not api_key or not cx:
            continue  # Skip if either is missing

        params = {
            'q': query,
            'key': api_key,
            'cx': cx,
            "num": max_results,
        }

        try:
            print(f"Searching Google with API key ending in {api_key[-4:]} and cx {cx}...")
            print("Starting search... for query: ", query)
            response = requests.get(url, params=params)
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

                print(f"Google Search for '{query}' with API key ending in {api_key[-4:]} and cx {cx}: Success")
                print(f"Total results: {len(arr)}")
                return True, arr  # Successful response

            else:
                print(f"No items found for API key ending with {api_key[-4:]} and cx {cx}.")

        except requests.exceptions.RequestException as e:
            print(f"API key ending with {api_key[-4:]} with cx {cx} failed: {e}")

    print("All API key and search engine ID combinations failed.")
    return False, arr
