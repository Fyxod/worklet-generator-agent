from app.utils.search_functions.duck import fetch_duckduckgo_results
from app.utils.search_functions.google_search import google_search
from app.utils.link_extractor import extract_content_from_link
import json
from concurrent.futures import ThreadPoolExecutor, as_completed


def search(queries: list, max_results: int = 5):
    try:
        results = []
        for query in queries:
            try:
                success, result = google_search(query=query, max_results=max_results)
                if success:
                    results.extend(result)
                    continue
                else:
                    print(
                        f"Google search failed for query: {query}. Trying DuckDuckGo."
                    )
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

        try:
            with open("search_results_unprocessed.json", "w") as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            print(f"Failed to write results to file. Error: {e}")

        # Extract content from links in parallel and format output
        def process_result(entry):
            try:
                link = entry.get("link")
                extracted = extract_content_from_link(link, 150) if link else ""
                return {
                    "page_title": entry.get("title", ""),
                    "page_body": f"{entry.get('body', '')} {extracted}",
                    "link": entry.get("link", ""),
                }
            except Exception as e:
                print(f"Error processing link: {link}. Error: {e}")
                return None

        processed_results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_result, entry) for entry in results]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    processed_results.append(result)

        try:
            with open("search_results_processed.json", "w") as f:
                json.dump(processed_results, f, indent=4)
        except Exception as e:
            print(f"Failed to write processed results to file. Error: {e}")

        return processed_results

    except Exception as e:
        print(f"An error occurred in the search function. Error: {e}")
        return []

queries = [
    "recent advancements in scene text recognition 2024-2025",
    "benchmark datasets for scene text recognition beyond ICDAR",
    "on-device AI optimization techniques for scene text recognition models",
    "transformer architectures for scene text recognition - latest research",
    "Generative AI applications for synthetic data generation in scene text recognition",
]

search(queries)