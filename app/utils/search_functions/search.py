from app.utils.search_functions.duck import fetch_duckduckgo_results, fetch_duckduckgo_references
from app.utils.search_functions.google_search import google_search, google_search_references
from app.utils.link_extractor import extract_content_from_link
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import time

start_time = time.time()

def search(queries: list, max_results: int = 5, word_limit: int = 150):
    """
    Perform a search using multiple search engines, process the results, and save the output.
    Args:
        queries (list): A list of search queries to execute.
        max_results (int, optional): The maximum number of results to fetch for each query. Defaults to 5.
        word_limit (int, optional): The maximum number of words to extract from the content of each result. Defaults to 150.
    Returns:
        list: A list of dictionaries containing the search query and its corresponding processed search results.
              Each dictionary has the following structure:
              {
                  "search_query": <query>,
                  "search_results": [
                      {
                          "page_title": <title of the page>,
                          "page_body": <processed content of the page>
                      },
                      ...
    Notes:
        - The function uses Google and DuckDuckGo as search engines.
        - Results are processed in parallel using a thread pool to extract content from links.
        - Processed results are grouped by search query and saved to a JSON file named "search_results_processed.json".
    Exceptions:
        - Logs errors encountered during search engine queries, content extraction, and file writing.
        - Returns an empty list if an unexpected error occurs during the entire process.
    """
    
    
    try:
        results = []
        # Fetch search results
        for query in queries:
            try:
                success, result = google_search(query=query, max_results=max_results)
                if success:
                    results.extend(result)
                    continue
            except Exception as e:
                print(f"Google search failed for query: {query}. Error: {e}")

            try:
                duck_results = fetch_duckduckgo_results(query=query, max_results=max_results)
                if duck_results:
                    results.extend(duck_results)
            except Exception as e:
                print(f"DuckDuckGo search failed for query: {query}. Error: {e}")
                
        # Parallel processing of all entries
        def process_entry(entry):
            try:
                link = entry.get("link")
                extracted = extract_content_from_link(link, word_limit=word_limit) if link else ""
                return {
                    "search_query": entry.get("query", ""),
                    "page_title": entry.get("title", ""),
                    "page_body": f"{entry.get('body', '')} {extracted}",
                    # "link": link,
                }
            except Exception as e:
                print(f"Error processing link: {entry.get('link')}. Error: {e}")
                return None

        all_processed = []
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(process_entry, entry) for entry in results]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_processed.append(result)

        # Regroup by search_query
        grouped_results = defaultdict(list)
        for item in all_processed:
            grouped_results[item["search_query"]].append({
                "page_title": item["page_title"],
                "page_body": item["page_body"],
                # "link": item["link"]
            })

        final_output = [
            {"search_query": query, "search_results": entries}
            for query, entries in grouped_results.items()
        ]

        # Save processed results
        try:
            with open("search_results_processed.json", "w") as f:
                json.dump(final_output, f, indent=4)
        except Exception as e:
            print(f"Failed to write processed results to file. Error: {e}")

        return final_output

    except Exception as e:
        return []


def search_references(keyword: str, max_results: int = 10):
    """
    Searches for references using multiple search engines and returns the results.
    This function attempts to fetch search results from Google and DuckDuckGo
    for the given keyword. If both searches fail, it returns an empty list.
    Optionally, the results can be saved to a JSON file.
    Args:
        keyword (str): The search keyword to query.
        max_results (int, optional): The maximum number of results to fetch. Defaults to 10.
    Returns:
        list: A list of search results. If no results are found or an error occurs, 
              an empty list is returned.
    Notes:
        - If the Google search fails, it attempts to fetch results from DuckDuckGo.
        - If both searches fail, the function returns an empty list.
        - Results are optionally saved to a JSON file named "search_results_references_extra.json".
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
        with open("search_results_references_extra.json", "w") as f:
            json.dump(results, f, indent=4)
        return results

    except Exception as e:
        return []