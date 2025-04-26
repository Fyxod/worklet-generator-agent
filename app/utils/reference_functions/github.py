import requests
import time

start_time = time.time()


def get_github_references(keyword):
    print("printing keyword inside github", keyword)
    url = "https://api.github.com/search/repositories"
    params = {"q": keyword, "per_page": 10}

    def make_request():
        return requests.get(url, params=params)

    response = make_request()

    if response.status_code != 200:
        time.sleep(1)
        response = make_request()

    if response.status_code == 200:
        data = response.json()
    result = []
    for item in data.get("items", []):
        description = item.get("description", "")
        if description:
            description = slice_to_100_words(description)
        else:
            description = ""
        result.append(
            {
                "Title": item["name"],
                "Description": description,
                "Link": item["html_url"],
                "Tag": "github",
            }
        )

        print("Github references insdie", result)
        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


def slice_to_100_words(text):
    words = text.split()
    if len(words) <= 100:
        return text
    else:
        return " ".join(words[:100])


# print(get_github_references("q learning"))
# keywords = [
#     'blizzard',
#     'encrypt malware',
#     'genai iot',
#     'deep q learning',
#     'deep reinforcement learning',
# ]
# from concurrent.futures import ThreadPoolExecutor

# with ThreadPoolExecutor() as executor:
#     results = list(executor.map(get_github_references, keywords))
#     for keyword, result in zip(keywords, results):
#         print(f"Keyword: {keyword}")
#         for item in result:
#             print(f"Title: {item['title']}, Description: {item['description']}, Link: {item['link']}")
#         print("\n")

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")
