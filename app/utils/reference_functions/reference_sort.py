from app.llm import invoke_llm
from app.utils.prompt_templates import refrence_sort_template
from app.utils.llm_response_parser import extract_json_from_llm_response
import json

def sort(worklet,model):
    print("printing worklet before sorting"*10)
    print(worklet["Reference Work"])
    reference_work_str = json.dumps(worklet['Reference Work'], indent=2)
    prompt =refrence_sort_template(reference_work_str)  
    # prompt = prompt_template.format(json=reference_work_str) # populte the prompt with worklet data
    sorted_references = invoke_llm(prompt, model)
    worklet["Reference Work"] = extract_json_from_llm_response(sorted_references)
    print("sorted worklet"*5, worklet["Reference Work"])
    return worklet
