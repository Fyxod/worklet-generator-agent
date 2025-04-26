from app.utils.reference_functions.scholar_package import CustomGoogleScholarOrganic

# from .scholar_package import CustomGoogleScholarOrganic


def get_google_scholar_references(keyword):
    try:
        print("printing google keyword inside", keyword)
        custom_parser_get_organic_results = (
            CustomGoogleScholarOrganic().scrape_google_scholar_organic_results(
                query=keyword, pagination=False, save_to_csv=False, save_to_json=True
            )
        )

        result = []
        for i in custom_parser_get_organic_results:
            title = i.get("title", "")
            title = (
                title.replace("[PDF]", "").replace("[HTML]", "").replace("[DOC]", "")
            )
            description = i.get("description", "")
            # if description:
            #     description = slice_to_100_words(description)
            # else:
            #     description = "did not find any discription just sort them sa u see fit try to keep one with tag scholar in front "
            result.append(
                {
                    "Title": title,
                    "Link": i.get("title_link", ""),
                    "Description": description,
                    "Tag": "scholar",
                }
            )
        print("google scholar inside", result)
        return result

    except Exception as e:
        print(f"Error while fetching Google Scholar references: {e}")
        return []


def slice_to_100_words(text):
    words = text.split()
    if len(words) <= 100:
        return text
    else:
        return " ".join(words[:100])


# example_usage()
# keywords = [
#     'blizzard',
#     'encrypt malware',
#     'genai iot',
#     'deep q learning',
#     'deep reinforcement learning',
# ]

# #using threads
# from concurrent.futures import ThreadPoolExecutor
# def fetch_data(keyword):
#     return CustomGoogleScholarOrganic().scrape_google_scholar_organic_results(
#         query=keyword,
#         pagination=False,
#         save_to_csv=False,
#         save_to_json=True
#     )
# with ThreadPoolExecutor(max_workers=5) as executor:
#     results = list(executor.map(fetch_data, keywords))
#     for result in results:
#         print(json.dumps(result, indent=2, ensure_ascii=False))
# end_time = time.time()
# print(f"Execution time: {end_time - start_time} seconds")
# # print(json.dumps(serpapi_parser_get_organic_results, indent=2, ensure_ascii=False))
# # print(json.dumps(top_publication_citation, indent=2, ensure_ascii=False))
