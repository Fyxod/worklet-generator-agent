import json

def extract_and_parse_first_dict(raw_text):
    stack = []
    start_idx = None
    # Clean up markdown-style formatting if it exists
    cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

    for i, char in enumerate(cleaned_text):
        if char == '{':
            if not stack:
                start_idx = i
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    dict_str = cleaned_text[start_idx:i+1]
                    try:
                        return json.loads(dict_str)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Found candidate but failed to parse JSON: {e}")
    
    raise ValueError("No valid JSON dictionary found in input.")
