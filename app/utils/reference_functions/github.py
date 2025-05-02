import requests
import time

def get_github_references(keyword):
    """
    Fetches a list of GitHub repositories based on a given keyword.
    This function queries the GitHub Search API to retrieve repositories
    matching the specified keyword. It returns a list of dictionaries
    containing repository details such as title, description, link, and tag.
    Args:
        keyword (str): The search keyword to query GitHub repositories.
    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - "Title" (str): The name of the repository.
            - "Description" (str): A truncated description of the repository (up to 100 words).
            - "Link" (str): The URL to the repository.
            - "Tag" (str): A fixed tag value ("github").
    Notes:
        - If the API request fails with a non-200 status code, the function retries once
          after a 1-second delay.
        - If the API request continues to fail, an error message is printed, and an empty
          list is returned.
        - The function assumes the presence of a helper function `slice_to_100_words`
          to truncate descriptions to 100 words.
    Raises:
        None: The function handles API errors internally and does not raise exceptions.
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

