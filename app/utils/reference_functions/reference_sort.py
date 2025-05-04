from app.llm import invoke_llm
from app.utils.prompt_templates import refrence_sort_template, index_sort_template
from app.utils.llm_response_parser import extract_dicts_smart
import json, os
import ast

output_directory = "sorted_references"
os.makedirs(output_directory, exist_ok=True)

def inplace_sort(worklet,model, index):
    """
    Take Input of a Single Worklet and sort the serefences on the basis of the discription 
    provided in Increasing order of Relevence

    """
    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt =refrence_sort_template(reference_work_str)  
    sorted_references = invoke_llm(prompt, model)
    filename = f"{index + 1}_Inplace_sort.json"
    path = os.path.join(output_directory, filename)
    worklet["Reference Work"] = extract_dicts_smart(sorted_references)
    with open(path, "w") as file:
        json.dump(worklet["Reference Work"], file, indent=4)
    return worklet

async def scholar_sort(worklet, model, index):
    """
    Take Input of a Single Worklet and sort the references on the basis of the description 
    provided in Increasing order of Relevance.
    """
    priority = {
        'scholar': 0,
        'google': 1,
        'github': 2
    }
    worklet["Reference Work"].sort(key=lambda x: priority.get(x['Tag'], 2))
    filename = f"{index + 1}_scholar_sort.json"
    path = os.path.join(output_directory, filename)
    
    with open(path, "w") as file:
        json.dump(worklet["Reference Work"], file, indent=4)

    return worklet


async def index_sort(worklet, model, index):
    """
    Take Input of a Single Worklet and sort the references on the basis of the description 
    provided in Increasing order of Relevance.
    """
    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt = index_sort_template(reference_work_str)  # Assuming this is defined elsewhere
    
    try:
        sorted_indices = await invoke_llm(prompt, model)  # Make sure invoke_llm is async
        print("LLM returned:", sorted_indices)
        
        sorted_indices = convert_to_list(sorted_indices)
        if sorted_indices == "failed":
            print("Index sort failed, falling back to scholar sort")
            return await scholar_sort(worklet, model, index)
        
        sorted_indices = remove_duplicates(sorted_indices)
        sorted_references = rearrange_references(worklet['Reference Work'], sorted_indices)

        filename = f"{index + 1}_index_sort.json"
        path = os.path.join(output_directory, filename)
        
        worklet["Reference Work"] = sorted_references
        
        with open(path, "w") as file:
            json.dump(worklet["Reference Work"], file, indent=4)

    except Exception as e:
        print(f"Error during index sorting: {e}")
        return await scholar_sort(worklet, model, index)
    
    return worklet

def rearrange_references(reference_work, sorted_indices):
    rearranged_references = []
    for i in sorted_indices:
        if 0 <= i < len(reference_work):
            rearranged_references.append(reference_work[i])
        else:
            print(f"Warning: Ignoring invalid index {i}")
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
        
        return "failed"

def remove_duplicates(numbers):
    """Removes duplicates from a list while keeping order."""
    seen = set()
    unique_numbers = []
    for num in numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)
    return unique_numbers
