from app.llm import invoke_llm
from app.utils.prompt_templates import refrence_sort_template
from app.utils.llm_response_parser import extract_json_from_llm_response
import json, os


output_directory = "sorted_references"
os.makedirs(output_directory, exist_ok=True)

def Inplace_sort(worklet,model, index):
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
    filename = f"{index + 1}.json"
    path = os.path.join(output_directory, filename)
    print("\n")
    worklet["Reference Work"] = extract_json_from_llm_response(sorted_references)
    with open(path, "w") as file:
        json.dump(worklet["Reference Work"], file, indent=4)
    print("sorted worklet"*5, worklet["Reference Work"])
    print("\n")
    return worklet


def Index_sort(worklet,model):
    """
    Take Input of a Single Worklet and sort the serefences on the basis of the discription 
    provided in Increasing order of Relevence

    """



def scholar_sort(worklet,model):
    """
    Take Input of a Single Worklet and sort the serefences on the basis of the discription 
    provided in Increasing order of Relevence
    """

