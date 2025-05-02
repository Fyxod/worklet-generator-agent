import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
api_keys = [
    os.getenv("GOOGLE_API_KEY1"),
    os.getenv("GOOGLE_API_KEY2"),
]

search_engine_ids = [
    os.getenv("SEARCH_ENGINE_ID1"),
    os.getenv("SEARCH_ENGINE_ID2"),
]

api_key_ref = os.getenv("GOOGLE_API_KEY_ref")
search_engine_id_ref = os.getenv("SEARCH_ENGINE_ID_ref")


url = 'https://www.googleapis.com/customsearch/v1'

def google_search(query, max_results=5):
    """
    Perform a Google Custom Search using multiple API keys and search engine IDs.

    This function iterates through a list of API keys and search engine IDs to perform
    a Google Custom Search for the given query. It returns the search results if successful.

    Args:
        query (str): The search query string.
        max_results (int, optional): The maximum number of results to retrieve. Defaults to 5.

    Returns:
        tuple: A tuple containing:
            - bool: True if the search was successful, False otherwise.
            - list: A list of dictionaries containing search results. Each dictionary contains:
                - "title" (str): The title of the search result.
                - "link" (str): The URL of the search result.
                - "body" (str): The snippet/description of the search result.
                - "query" (str): The original search query.
    """
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

                return True, arr

        except requests.exceptions.RequestException as e:
            print(f"API key ending with {api_key[-4:]} with cx {cx} failed: {e}")

    return False, arr

def google_search_references(query, max_results=10):
    """
    Perform a Google Custom Search for references using a specific API key and search engine ID.

    This function uses a dedicated API key and search engine ID to perform a Google Custom Search
    for the given query. It is intended for retrieving reference-related search results.

    Args:
        query (str): The search query string.
        max_results (int, optional): The maximum number of results to retrieve. Defaults to 10.

    Returns:
        tuple: A tuple containing:
            - bool: True if the search was successful, False otherwise.
            - list: A list of dictionaries containing search results. Each dictionary contains:
                - "Title" (str): The title of the search result.
                - "Link" (str): The URL of the search result.
                - "Description" (str): The snippet/description of the search result.
                - "Tag" (str): A tag indicating the source of the result (e.g., "google").
    """
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
    