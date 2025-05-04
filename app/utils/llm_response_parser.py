import json

def extract_dicts_smart(raw_text):
    stack = []
    start_idx = None
    results = []

    # Clean up markdown-style formatting if it exists
    cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

    for i, char in enumerate(cleaned_text):
        if char == '{':
            if not stack:
                start_idx = i  # Start of a new top-level dict
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start_idx is not None:
                    dict_str = cleaned_text[start_idx:i+1]
                    try:
                        parsed = json.loads(dict_str)
                        results.append(parsed)
                    except json.JSONDecodeError:
                        pass  # Skip malformed dicts

    if not results:
        raise ValueError("No valid JSON dictionaries found in input.")
    
    # Smart return
    return results[0] if len(results) == 1 else results
