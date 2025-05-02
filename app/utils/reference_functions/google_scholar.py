from app.utils.reference_functions.scholar_package import CustomGoogleScholarOrganic

def get_google_scholar_references(keyword):
    """
    Fetches Google Scholar references related to the given keyword.
    Returns a list of dictionaries containing the title, description, link, and tag.
    """
    try:
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
            description = i.get("snippet", "")
            if description:
                description = slice_to_100_words(description)
            else:
                description = "Did not find any description for this paper just sort them as you see fit try to keep one with tag scholar in front"
            result.append(
                {
                    "Title": title,
                    "Link": i.get("title_link", ""),
                    "Description": description,
                    "Tag": "scholar",
                }
            )
        return result

    except Exception as e:
        print(f"Error while fetching Google Scholar references: {e}")
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

