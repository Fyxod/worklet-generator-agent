import ast
import json

from app.llm import invoke_llm
from app.utils.llm_response_parser import extract_dicts_smart
from app.utils.prompt_templates import reference_sort_template, index_sort_template


def inplace_sort(worklet,model):
    """
    Sorts the 'Reference Work' entries within a worklet in place using an LLM-based sorting mechanism.
    Args:
        worklet (dict): A dictionary containing a 'Reference Work' key with references to be sorted.
        model (Any): The language model to be used for sorting the references.
    Returns:
        dict: The updated worklet dictionary with the 'Reference Work' entries sorted.
    Raises:
        KeyError: If 'Reference Work' key is not present in the worklet.
        Exception: If the LLM invocation or extraction of sorted references fails.
    """

    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt =reference_sort_template(reference_work_str)  
    sorted_references = invoke_llm(prompt, model)
    worklet["Reference Work"] = extract_dicts_smart(sorted_references)
    return worklet


async def scholar_sort(worklet):
    """
    Sorts the "Reference Work" list in the given worklet dictionary based on the priority of the 'Tag' field.
    The sorting priority is as follows:
        - 'scholar': 0 (highest priority)
        - 'google': 1
        - 'github': 2 (lowest priority)
    Any tag not listed will be assigned the lowest priority (2).
    Args:
        worklet (dict): A dictionary containing a "Reference Work" key, which maps to a list of references. 
                        Each reference is expected to be a dictionary with a 'Tag' key.
    Returns:
        dict: The input worklet dictionary with its "Reference Work" list sorted by tag priority.
    """

    priority = {
        'scholar': 0,
        'google': 1,
        'github': 2
    }
    worklet["Reference Work"].sort(key=lambda x: priority.get(x['Tag'], 2))

    return worklet


async def index_sort(worklet, model):
    """
    Asynchronously sorts the 'Reference Work' entries in a worklet using an LLM-based index sorting approach.
    Args:
        worklet (dict): A dictionary containing a 'Reference Work' key with a list of references to be sorted.
        model (str): The identifier or name of the language model to use for sorting.
    Returns:
        dict: The updated worklet dictionary with the 'Reference Work' list sorted according to the LLM's output.
              If the LLM-based sorting fails, falls back to scholar_sort for sorting.
    Raises:
        Exception: If an unexpected error occurs during the sorting process, the function falls back to scholar_sort.
    """

    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt = index_sort_template(reference_work_str)
    
    try:
        sorted_indices = await invoke_llm(prompt, model)

        sorted_indices = convert_to_list(sorted_indices)
        if sorted_indices == "failed":
            print("Index sort failed, falling back to scholar sort")
            return await scholar_sort(worklet)

        sorted_indices = remove_duplicates(sorted_indices)
        sorted_references = rearrange_references(worklet['Reference Work'], sorted_indices)

        worklet["Reference Work"] = sorted_references

    except Exception as e:
        print(f"Error during index sorting: {e}")
        return await scholar_sort(worklet)

    return worklet


def rearrange_references(reference_work, sorted_indices):
    """
    Rearranges the elements of reference_work according to the order specified in sorted_indices.
    Args:
        reference_work (list): The list of references to be rearranged.
        sorted_indices (list of int): The list of indices specifying the new order.
    Returns:
        list: A new list of references rearranged as per sorted_indices.
    """

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
