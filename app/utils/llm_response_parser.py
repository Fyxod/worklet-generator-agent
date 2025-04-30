import json

def extract_json_from_llm_response(llm_response):
    """
    Extracts and converts a JSON-like response from an LLM into a valid JSON object.

    :param llm_response: A string with the JSON wrapped in backticks.
    :return: Parsed JSON object (dictionary)
    """
    
    raw_json_string = llm_response
     
     
     
    print( " \ninput to extractor below------------- "*2,"\n" )
    print(raw_json_string)
    # Remove backticks and "json" keyword if present
    cleaned_json_string = raw_json_string.replace("```json", "").replace("```", "").strip()
    print(cleaned_json_string)
    print("\n","try---"*10,"\n")
    
    try:
        print("\n inside try"*5)
        parsed_json = json.loads(cleaned_json_string)
        print("\n","returning this ---"*10,"\n")
        print(parsed_json)
        return parsed_json
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")

