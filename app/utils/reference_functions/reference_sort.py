from app.llm import invoke_llm
from app.utils.prompt_templates import refrence_sort_template, index_sort_template
from app.utils.llm_response_parser import extract_json_from_llm_response
import json, os
import ast

output_directory = "sorted_references"
os.makedirs(output_directory, exist_ok=True)

def inplace_sort(worklet,model, index):
    """
    Take Input of a Single Worklet and sort the serefences on the basis of the discription 
    provided in Increasing order of Relevence

    """
    print("-"*10+"printing worklet before sorting"*10+"-"*10)
    print("\n")
    print("\n")
    print(worklet["Reference Work"])
    print("\n")
    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt =refrence_sort_template(reference_work_str)  
    sorted_references = invoke_llm(prompt, model)
    print("Printing Sorted array of ref")
    print("\n")
    print("dumped sorted references")
    #dump to file name index.json
    filename = f"{index + 1}_Inplace_sort.json"
    path = os.path.join(output_directory, filename)
    print("\n")
    worklet["Reference Work"] = extract_json_from_llm_response(sorted_references)
    with open(path, "w") as file:
        json.dump(worklet["Reference Work"], file, indent=4)
    print("sorted worklet"*5, worklet["Reference Work"])
    print("\n")
    return worklet

def scholar_sort(worklet,model,index):
    """
    Take Input of a Single Worklet and sort the serefences on the basis of the discription 
    provided in Increasing order of Relevence
    """
    print("-"*10+"printing worklet before sorting"*10+"-"*10)
    print("\n")
    print("\n")
    print(worklet["Reference Work"])
    print("\n")
##   Actual sorting taking place
    priority = {
    'scholar': 0,
    'github': 1
}
    worklet["Reference Work"].sort(key=lambda x: priority.get(x['Tag'], 2))

    print("Printing Sorted array of ref")
    print("\n")
    print("dumped sorted references")
    #dump to file name index.json
    filename = f"{index + 1}_scholar_sort.json"
    path = os.path.join(output_directory, filename)
    print("\n")
    print("\n")
    with open(path, "w") as file:
        json.dump(worklet["Reference Work"], file, indent=4)
    print("sorted worklet"*5, worklet["Reference Work"])
    print("\n")
    print("\n")
    print("scholar Sort Used -------------------"*10)
    print("\n")
    
    return worklet

def index_sort(worklet,model,index):
    """
    Take Input of a Single Worklet and sort the serefences on the basis of the discription 
    provided in Increasing order of Relevence

    """

    print("\n")
    print("-"*10+"printing worklet before sorting"*10+"-"*10)
    print("\n")
    print(worklet["Reference Work"])
    print("\n")
    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt =index_sort_template(reference_work_str)  
    sorted_indices = invoke_llm(prompt, model)
    print("\n")
    print(sorted_indices)
    print("\n")
    sorted_indices=convert_to_list(sorted_indices)
    if sorted_indices :
        return scholar_sort(worklet,model,index)

    sorted_indices=remove_duplicates(sorted_indices)
    sorted_references = rearrange_references(worklet['Reference Work'], sorted_indices)
    print("Printing Sorted array of ref")
    print("\n")
    print("dumped sorted references")
    print("\n")
    #dump to file name index.json
    filename = f"{index + 1}_index_sort.json"
    path = os.path.join(output_directory, filename)
    print("\n")
    worklet["Reference Work"] = sorted_references
    with open(path, "w") as file:
        json.dump(worklet["Reference Work"], file, indent=4)
    print("\n")
    print("sorted worklet"*5, worklet["Reference Work"])
    print("\n")
    print("Index Sort Used -------------------"*10)
    print("\n")
    return worklet


def rearrange_references(reference_work, sorted_indices):
    rearranged_references = [reference_work[i] for i in sorted_indices]
    return rearranged_references

def convert_to_list(input_data):
    """
    Convert input_data to a list of integers safely.

    Handles:
    - Lists of integers directly.
    - Strings that are valid JSON lists (e.g., "[1, 2, 3]").
    - Strings containing a list inside text (e.g., "abc [1,2,3] xyz").
    - Strings of numbers separated by commas or spaces (e.g., "1,2,3" or "1 2 3").

    If parsing fails, returns True and prints a warning.
    """

    try:
        if isinstance(input_data, list):
            return [int(x) for x in input_data]

        elif isinstance(input_data, str):
            input_data = input_data.strip()

            # Try JSON loading first
            try:
                parsed = json.loads(input_data)
                if isinstance(parsed, list):
                    return [int(x) for x in parsed]
            except json.JSONDecodeError:
                pass

            # Try to find a list inside the string (e.g., "some text [1,2,3]")
            if '[' in input_data and ']' in input_data:
                start = input_data.find('[')
                end = input_data.find(']', start) + 1
                list_str = input_data[start:end]
                try:
                    parsed = ast.literal_eval(list_str)
                    if isinstance(parsed, list):
                        return [int(x) for x in parsed]
                except (ValueError, SyntaxError):
                    pass

            # Fallback: split by common separators
            separators = [",", " "]
            for sep in separators:
                if sep in input_data:
                    parts = input_data.split(sep)
                    return [int(x.strip()) for x in parts if x.strip().isdigit()]

        # If nothing worked
        raise ValueError

    except (ValueError, TypeError):
        print("Warning: Input could not be parsed. Using default list [1, 2, 3, 4, 5].")
        return True

def remove_duplicates(numbers):
    """Removes duplicates from a list while keeping order."""
    seen = set()
    unique_numbers = []
    for num in numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)
    return unique_numbers