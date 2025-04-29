from duckduckgo_search import DDGS
import time


def fetch_duckduckgo_results(query: str, max_results: int = 5, max_retries: int = 10,delay_after_req: float=0.75, delay_exception: int = 3):
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
    attempt = 0
    ddgs = DDGS()
    arr=[]
    while attempt < max_retries:
        try:
            results = list(ddgs.text(query, max_results=max_results))

            if results and isinstance(results, list):
                print(f"Search for '{query}': Success")
                for result in results:
                    if 'title' in result and 'href' in result:
                        arr.append({
                            "title": result['title'],
                            "link": result['href'],
                            "body": result.get('body', ''),
                            "query": query,
                        })
                print(f"Results for '{query}': {len(arr)}")
                print(f"Duckduckgo Total results: {len(arr)}")
                return arr  # Successful response
            else:
                print(f"No results found. Retrying in {delay_after_req} seconds...")
                time.sleep(delay_after_req)
                attempt += 1

        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {delay_exception} seconds...")
            time.sleep(delay_exception)
            attempt += 1

    print(f"Search for '{query}' failed after {max_retries} attempts.")
    return []





search =[
        "recent advancements in scene text recognition 2024-2025",
        "benchmark datasets for scene text recognition beyond ICDAR",
        "on-device AI optimization techniques for scene text recognition models",
        "transformer architectures for scene text recognition - latest research",
        "Generative AI applications for synthetic data generation in scene text recognition",
]
def jj():
    {
        "title": "A comprehensive survey of deep learning-based lightweight object ...",
        "href": "https://link.springer.com/article/10.1007/s10462-024-10877-1",
        "body": "This study concentrates on deep learning-based lightweight object detection models on edge devices. Designing such lightweight object recognition models is more difficult than ever due to the growing demand for accurate, quick, and low-latency models for various edge devices. The most recent deep learning-based lightweight object detection methods are comprehensively described in this work ...",
    },
    {
        "title": "PDF",
        "href": "https://link.springer.com/content/pdf/10.1007/s10462-024-10877-1.pdf",
        "body": "Abstract This study concentrates on deep learning-based lightweight object detection models on edge devices. Designing such lightweight object recognition models is more dificult than ever due to the growing demand for accurate, quick, and low-latency models for various edge devices.",
    },
    {
        "title": "Top Object Detection Models in 2024 - Ikomia",
        "href": "https://www.ikomia.ai/blog/top-object-detection-models-review",
        "body": "Explore the best object detection models for 2024, including YOLO, RTMDet, and RT-DETR. Find the ideal model for your project's needs.",
    },
    {
        "title": "High-precision and lightweight small-target detection ... - Nature",
        "href": "https://www.nature.com/articles/s41598-024-75243-1",
        "body": "While these studies have improved detection speed and reduced parameters for lightweight models in embedded devices, the detection accuracy in real-world applications still requires improvement.",
    },
    {
        "title": "SOD-YOLO: A lightweight small object detection framework",
        "href": "https://www.nature.com/articles/s41598-024-77513-4",
        "body": "With the advancement of edge computing devices, an increasing number of lightweight small object detection algorithms now prioritize inference speed on parallel computing edge devices.",
    }
