import time
from duckduckgo_search import DDGS


def fetch_duckduckgo_results(
    query: str,
    max_results: int = 5,
    max_retries: int = 10,
    delay_after_req: float = 0.75,
    delay_exception: int = 3,
):
    """
    Searches DuckDuckGo for a given query and returns JSON results.

    Args:
        query (str): The search term.
        max_results (int): Maximum number of results to fetch.
        max_retries (int): Number of times to retry in case of failure.
        delay_after_req (int): Seconds to wait between retries.
        delay_exception (int): Seconds to wait between retries.

    Returns:
        list: A list of search results (each result is a dictionary).
              Returns an empty list if all retries fail.
    """
    print(f"Fetching DuckDuckGo results for query: {query}")
    attempt = 0
    ddgs = DDGS()
    arr = []
    while attempt < max_retries:
        try:
            results = list(ddgs.text(query, max_results=max_results))

            if results and isinstance(results, list):
                for result in results:
                    if "title" in result and "href" in result:
                        arr.append(
                            {
                                "title": result["title"],
                                "link": result["href"],
                                "body": result.get("body", ""),
                                "query": query,
                            }
                        )
                return arr
            else:
                time.sleep(delay_after_req)
                attempt += 1

        except Exception as e:
            time.sleep(delay_exception)
            attempt += 1

    return []


def fetch_duckduckgo_references(query: str, max_results: int = 5):
    """
    Fetches search results from DuckDuckGo using the DDGS library.
    Args:
        query (str): The search query string.
        max_results (int, optional): The maximum number of search results to fetch. Defaults to 5.
    Returns:
        list: A list of dictionaries containing search result details. Each dictionary includes:
            - "Title" (str): The title of the search result.
            - "Link" (str): The URL of the search result.
            - "Description" (str): A brief description or body of the search result (if available).
            - "Tag" (str): A fixed tag value ("google").
        If no results are found or an error occurs, an empty list is returned.
    Raises:
        Exception: If an error occurs during the search process, it is caught and logged.
    """

    ddgs = DDGS()
    arr = []
    try:
        results = list(ddgs.text(query, max_results=max_results))

        if results and isinstance(results, list):
            for result in results:
                if "title" in result and "href" in result:
                    arr.append(
                        {
                            "Title": result["title"],
                            "Link": result["href"],
                            "Description": result.get("body", ""),
                            "Tag": "google",
                        }
                    )
            return arr
        else:
            return
    except Exception as e:
        return []
