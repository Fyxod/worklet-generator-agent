from app.utils.search_functions.duck import fetch_duckduckgo_results, fetch_duckduckgo_references
from app.utils.search_functions.google_search import google_search, google_search_references
from app.utils.link_extractor import extract_content_from_link
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import time

start_time = time.time()

def search(queries: list, max_results: int = 5, word_limit: int = 300):
    try:
        results = []

        # Fetch search results
        for query in queries:
            try:
                success, result = google_search(query=query, max_results=max_results)
                if success:
                    results.extend(result)
                    continue
                else:
                    print(f"Google search failed for query: {query}. Trying DuckDuckGo.")
            except Exception as e:
                print(f"Google search failed for query: {query}. Error: {e}")

            try:
                duck_results = fetch_duckduckgo_results(query=query, max_results=max_results)
                if duck_results:
                    results.extend(duck_results)
                else:
                    print(f"DuckDuckGo search failed for query: {query}.")
            except Exception as e:
                print(f"DuckDuckGo search failed for query: {query}. Error: {e}")

        print(f"Total results from all searches: {len(results)}")

        # Save raw results
        try:
            with open("search_results_unprocessed.json", "w") as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            print(f"Failed to write results to file. Error: {e}")

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
        print(f"An error occurred in the search function. Error: {e}")
        return []


def search_references(keyword: str, max_results: int = 10):
    try:
        results = []
        try:
            success, result = google_search_references(query=keyword, max_results=max_results)
            if success:
                results.extend(result)
                return results
            else:
                print(f"Google search failed for keyword: {keyword}. Trying DuckDuckGo.")
        except Exception as e:
            print(f"Google search failed for keyword: {keyword}. Error: {e}")

        try:
            duck_results = fetch_duckduckgo_references(query=keyword, max_results=max_results)
            if duck_results:
                results.extend(duck_results)
                return results
            else:
                print(f"DuckDuckGo search failed for keyword: {keyword}.")
        except Exception as e:
            print(f"DuckDuckGo search failed for keyword: {keyword}. Error: {e}")
            return results
        with open("search_results_references_extra.json", "w") as f:
            json.dump(results, f, indent=4)
        print(results)
        return results

    except Exception as e:
        print(f"An error occurred in the search function. Error: {e}")
        return []


# search_references("scene text recognition", max_results=5)


queries = [
    "recent advancements in scene text recognition 2024-2025",
    "benchmark datasets for scene text recognition beyond ICDAR",
    "on-device AI optimization techniques for scene text recognition models",
    "transformer architectures for scene text recognition - latest research",
    "Generative AI applications for synthetic data generation in scene text recognition",
]

# search(queries)

# end_time = time.time()
# print(f"Execution time: {end_time - start_time:.2f} seconds")