from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.utils.link_extractor import extract_content_from_link
from app.utils.search_functions.duck import fetch_duckduckgo_references, fetch_duckduckgo_results
from app.utils.search_functions.google_search import google_search, google_search_references


def search(queries: list, max_results: int = 5, word_limit: int = 300):
    """
    Performs a search operation using multiple search engines and processes the results.
    Args:
        queries (list): A list of search queries to execute.
        max_results (int, optional): The maximum number of results to fetch for each query. Defaults to 5.
        word_limit (int, optional): The maximum number of words to extract from each result's content. Defaults to 300.
    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - "search_query" (str): The original search query.
            - "search_results" (list): A list of dictionaries for each search result, containing:
                - "page_title" (str): The title of the page.
                - "page_body" (str): The body content of the page (including extracted content).
    Notes:
        - The function attempts to fetch results from Google and DuckDuckGo.
        - Results are processed in parallel using a thread pool for efficiency.
        - If an error occurs during any stage of the process, it is logged, and the function continues with the remaining queries.
        - The results are grouped by the original search query.
    """

    try:
        # return ["no web search results found"]
        results = []

        # Fetch search results
        for query in queries:
            try:
                success, result = google_search(query=query, max_results=max_results)
                if success:
                    for r in result:
                        r["query"] = query
                    results.extend(result)
                    continue
            except Exception as e:
                print(f"Google search failed for query: {query}. Error: {e}")

            try:
                duck_results = fetch_duckduckgo_results(query=query, max_results=max_results)
                if duck_results:
                    for r in duck_results:
                        r["query"] = query
                    results.extend(duck_results)
            except Exception as e:
                print(f"DuckDuckGo search failed for query: {query}. Error: {e}")

        # Group results by query
        grouped = defaultdict(list)
        for entry in results:
            grouped[entry.get("query", "")].append(entry)

        # Flatten the results again with word_limit info
        entries_with_limit = []
        for query, entries in grouped.items():
            for i, entry in enumerate(entries):
                limit = 800 if i < 1 else word_limit
                entries_with_limit.append((entry, limit))

        # Process entries in parallel
        def process_entry(entry, word_limit_in):
            try:
                link = entry.get("link")
                extracted = (
                    extract_content_from_link(link, word_limit=word_limit_in)
                    if link
                    else ""
                )
                return {
                    "search_query": entry.get("query", ""),
                    "page_title": entry.get("title", ""),
                    "page_body": f"{entry.get('body', '')} {extracted}",
                }
            except Exception:
                return None

        all_processed = []
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [
                executor.submit(process_entry, entry, limit)
                for entry, limit in entries_with_limit
            ]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_processed.append(result)

        # Regroup by search_query
        grouped_results = defaultdict(list)
        for item in all_processed:
            grouped_results[item["search_query"]].append(
                {
                    "page_title": item["page_title"],
                    "page_body": item["page_body"],
                    # "link": item["link"]
                }
            )

        final_output = [
            {"search_query": query, "search_results": entries}
            for query, entries in grouped_results.items()
        ]

        return final_output

    except Exception as e:
        print(f"Overall search error: {e}")
        return []


def search_references(keyword: str, max_results: int = 10):
    """
    Searches for references related to a given keyword using multiple search engines.
    Attempts to retrieve search results from Google first. If Google search fails,
    it falls back to DuckDuckGo. Returns a list of references found, up to the specified
    maximum number of results.
    Args:
        keyword (str): The search term to query.
        max_results (int, optional): The maximum number of results to return. Defaults to 10.
    Returns:
        list: A list of references found for the given keyword. Returns an empty list if no results are found or if all searches fail.
    """

    try:
        results = []
        try:
            success, result = google_search_references(query=keyword, max_results=max_results)
            if success:
                results.extend(result)
                return results
        except Exception as e:
            print(f"Google search failed for keyword: {keyword}. Error: {e}")

        try:
            duck_results = fetch_duckduckgo_references(query=keyword, max_results=max_results)
            if duck_results:
                results.extend(duck_results)
                return results

        except Exception as e:
            return results

        return results

    except Exception as e:
        return []
