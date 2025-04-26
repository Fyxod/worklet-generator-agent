from app.llm import invoke_llm
from app.utils.prompt_templates import refrence_sort_template


def sort(worklet,model):
    prompt_template =refrence_sort_template()  
    prompt = prompt_template.format(json=worklet) # populte the prompt with worklet data
    sorted_worklet = invoke_llm(prompt, model)
    return sorted_worklet
