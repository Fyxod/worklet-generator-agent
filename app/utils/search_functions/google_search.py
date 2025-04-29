import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY_DEVANSH")
SEARCH_ENGINE_ID =os.getenv("SEARCH_ENGINE_ID")
print("API_KEY", API_KEY)
print("SEARCH_ENGINE_ID", SEARCH_ENGINE_ID)

import requests
search_query = "transformer architectures for scene text recognition - latest research"
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
    print(results['items'])
    #dump to json file
    with open('search_results.json', 'w') as f:
        json.dump(results['items'], f, indent=4)
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
