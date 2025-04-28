from app.utils.llm_response_parser import extract_json_from_llm_response
from app.llm import invoke_llm
from app.utils.prompt_templates import worklet_gen_prompt    # all the prompts used in this projects were moved to prompt_templates
from app.socket import sio
async def generate_worklets(worklet_data, linksData, model, sid):
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
    
    try:
        generated_worklets = invoke_llm(prompt, model)
    except Exception as e:
        print("Error in generating worklets:", e)
        await sio.emit("error", {"message": "ERROR: LLM is not responding. Please try again."}, to=sid)

    # extracted_worklets = []
    try:
        extracted_worklets = extract_json_from_llm_response(generated_worklets)# remove back ticks
    except Exception as e:
        print("Error in extracting worklets:", e)
        await sio.emit("error", {"message": "ERROR: Wrong output returned by llm. Please try again."}, to=sid)
        
    return extracted_worklets
