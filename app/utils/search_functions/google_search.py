import requests
import os

SEARCH_ENGINE_ID = os.getenv("GOOGLE_API_KEY_DEVANSH"),
API_KEY =os.getenv("SEARCH_ENGIEN_ID")


import requests
search_query ="hi i want the most used language in world"
url = 'https://www.googleapis.com/customsearch/v1'
params = {
    'q': search_query,             # your search term
    'key': API_KEY,                 # your API key
    'cx': SEARCH_ENGINE_ID,         # your search engine ID
    # 'searchType': 'image'           # search for images
}

# try:
response = requests.get(url, params=params)
response.raise_for_status()  # raises an HTTPError if the response code was unsuccessful
results = response.json()  
if 'items' in results and results['items']:
    print(results['items'][0]['link'])
else:
    print("No items found in the search results.")

# except requests.exceptions.HTTPError as errh:
#     print(f"HTTP Error: {errh}")
# except requests.exceptions.ConnectionError as errc:
#     print(f"Connection Error: {errc}")
# except requests.exceptions.Timeout as errt:
#     print(f"Timeout Error: {errt}")
# except requests.exceptions.RequestException as err:
#     print(f"Unexpected Error: {err}")
# except KeyError:
#     print("Expected key not found in the response.")
