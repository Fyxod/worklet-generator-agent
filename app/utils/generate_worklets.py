from app.utils.llm_response_parser import extract_json_from_llm_response
from app.llm import invoke_llm
from app.utils.prompt_templates import worklet_gen_prompt    # all the prompts used in this projects were moved to prompt_templates
async def generate_worklets(worklet_data, linksData, model):
    """
    This function is used to ccommunicate with the llm model it 
    takes  worklet data and the model name as input 
    and return the worklets in a json format 

    """
    count = 6
    count_string = "six"
    if model == "gemini-flash-2.0":
        count = 5
        count_string = "five"
    
    prompt_template = worklet_gen_prompt()  
    prompt = prompt_template.format(worklet_data=worklet_data,linksData=linksData, count=count, count_string=count_string) # populte the prompt with worklet data
    generated_worklets = invoke_llm(prompt, model)

    extracted_worklets = extract_json_from_llm_response(generated_worklets)# remove back ticks
    return extracted_worklets
