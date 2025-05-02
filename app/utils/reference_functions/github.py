import requests
import time

def get_github_references(keyword):
    """
    Fetches GitHub repositories related to the given keyword.
    Returns a list of dictionaries containing the title, description, link, and tag.
    """
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

        return result
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


def slice_to_100_words(text):
    """
    Slices the text to the first 100 words.
    """
    words = text.split()
    if len(words) <= 100:
        return text
    else:
        return " ".join(words[:100])

