import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 4 api keys - 400 requests per day after which it'll fall back to duckduckgo search
api_keys = [
    os.getenv("GOOGLE_API_KEY4"),
    os.getenv("GOOGLE_API_KEY2"),
    os.getenv("GOOGLE_API_KEY1"),
    os.getenv("GOOGLE_API_KEY3"),
]

search_engine_ids = [
    os.getenv("SEARCH_ENGINE_ID4"),
    os.getenv("SEARCH_ENGINE_ID2"),
    os.getenv("SEARCH_ENGINE_ID1"),
    os.getenv("SEARCH_ENGINE_ID3"),
]

api_key_ref = os.getenv("GOOGLE_API_KEY_ref")
search_engine_id_ref = os.getenv("SEARCH_ENGINE_ID_ref")


url = "https://www.googleapis.com/customsearch/v1"


def google_search(query, max_results=10):
    """
    Performs a Google Custom Search using multiple API keys and search engine IDs, returning search results for a given query.
    Args:
        query (str): The search query string.
        max_results (int, optional): Maximum number of results to retrieve per request. Defaults to 10.
    Returns:
        tuple:
            - bool: True if search results were found and returned, False otherwise.
            - list: A list of dictionaries containing search result data with keys 'title', 'link', 'body', and 'query'.
    Notes:
        - Iterates through available API keys and search engine IDs, skipping any that are missing.
        - Handles rate limiting (HTTP 429) by skipping the affected API key.
        - Returns as soon as results are found from a successful API call.
        - If all API keys fail or no results are found, returns False and an empty list.
    """

    arr = []

    for api_key, cx in zip(api_keys, search_engine_ids):
        if not api_key or not cx:
            continue

        params = {
            "q": query,
            "key": api_key,
            "cx": cx,
            "num": max_results,
        }

        try:
            response = requests.get(url, params=params, timeout=6)

            if response.status_code == 429:
                print(f"Rate limit hit for API key ending with {api_key[-4:]}. Skipping.")
                continue

            response.raise_for_status()
            results = response.json()
            print(f"API key ending with {api_key[-4:]} with cx {cx} succeeded.")

            if "items" in results and results["items"]:
                for item in results["items"]:
                    arr.append(
                        {
                            "title": item.get("title"),
                            "link": item.get("link"),
                            "body": item.get("snippet"),
                            "query": query,
                        }
                    )

                return True, arr

        except requests.exceptions.RequestException as e:
            print(f"API key ending with {api_key[-4:]} with cx {cx} failed: {e}")

    # If all API keys fail, return an empty list
    return False, arr


def google_search_references(query, max_results=10):
    """
    Performs a Google Custom Search for references based on the provided query.
    Args:
        query (str): The search query string.
        max_results (int, optional): The maximum number of search results to retrieve. Defaults to 10.
    Returns:
        tuple: A tuple containing a boolean indicating success, and a list of dictionaries with search result details.
            Each dictionary contains:
                - "Title" (str): The title of the search result.
                - "Link" (str): The URL of the search result.
                - "Description" (str): A snippet/description of the search result.
                - "Tag" (str): A tag indicating the source ("google").
    Notes:
        - Requires valid `api_key_ref`, `search_engine_id_ref`, and `url` variables to be defined in the scope.
        - Returns (False, []) if the request fails or no results are found.
    """

    arr = []

    params = {
        "q": query,
        "key": api_key_ref,
        "cx": search_engine_id_ref,
        "num": max_results,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        if "items" in results and results["items"]:
            for item in results["items"]:
                arr.append(
                    {
                        "Title": item.get("title"),
                        "Link": item.get("link"),
                        "Description": item.get("snippet"),
                        "Tag": "google",
                    }
                )

            return True, arr

    except requests.exceptions.RequestException as e:
        return False, arr
