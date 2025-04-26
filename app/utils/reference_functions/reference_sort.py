from app.llm import invoke_llm



prompt_template = worklet_gen_prompt()  
    prompt = prompt_template.format(worklet_data=worklet_data,linksData=linksData) # populte the prompt with worklet data
    generated_worklets = invoke_llm(prompt, model)