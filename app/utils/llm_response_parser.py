import json


def extract_dicts_smart(raw_text, return_first):
    """
    Extracts JSON dictionaries from a raw text input.
    This function processes a given raw text, identifies JSON-like dictionary structures,
    and attempts to parse them into Python dictionaries. It handles cases where multiple
    JSON dictionaries are present in the input and returns either a single dictionary
    or a list of dictionaries.
    Args:
        raw_text (str): The input text containing JSON-like dictionary structures.
    Returns:
        dict or list: A single dictionary if one valid JSON dictionary is found,
                      or a list of dictionaries if multiple valid JSON dictionaries are found.
    Raises:
        ValueError: If no valid JSON dictionaries are found in the input.
    Notes:
        - The function removes any occurrences of "```json" and "```" from the input text
          before processing.
        - If the input contains malformed JSON, those parts are ignored.
    """

    stack = []
    start_idx = None
    results = []

    cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

    for i, char in enumerate(cleaned_text):
        if char == "{":
            if not stack:
                start_idx = i
            stack.append("{")
        elif char == "}":
            if stack:
                stack.pop()
                if not stack and start_idx is not None:
                    dict_str = cleaned_text[start_idx : i + 1]
                    try:
                        parsed = json.loads(dict_str)
                        results.append(parsed)
                    except json.JSONDecodeError:
                        pass

    if not results:
        raise ValueError("No valid JSON dictionaries found in input.")

    if return_first:
        return results[0]
    return results[0] if len(results) == 1 else results
