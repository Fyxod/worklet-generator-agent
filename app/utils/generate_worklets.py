from langchain.prompts import ChatPromptTemplate
from app.llm import llm
# from app.utils.llm_response_parser import extract_json_from_llm_response


def get_prompt_template():
    return ChatPromptTemplate.from_template("""You are an expert in analyzing and generating structured worklet ideas. Your task is to generate **five new worklets** based on the provided examples.  
### 🔹 **Instructions:**
- Ensure that the new worklets are **unique yet thematically aligned** with the given worklets.
- **Follow the exact format** below for each new worklet.
- **Do not fabricate unrealistic or fictional ideas**—keep them practical and feasible.
- **Exclude specific names of people, organizations, or brands**.

---

### ** Structure of Each Worklet Idea:**
1. **Problem Statement**: Clearly describe the problem this worklet aims to address.
2. **Goal**: Define the objective and intended outcome.
3. **Expectations**: Describe what participants are expected to do or accomplish.
4. **Training/Prerequisite**: List any required knowledge, skills, or prior learning needed.

---

### ** Existing Worklets for Reference:**
{worklet_data}

---

### ** Additional Guidelines:**
**Maintain originality**—do not copy or modify existing worklets too closely.  
**Keep ideas well-structured and clear** to ensure easy comprehension.  
**Avoid redundancy**—ensure each generated worklet introduces a fresh perspective.  
**Ensure coherence and practicality**—ideas should be applicable in real-world scenarios.  
**Do not introduce unrelated topics**—stick to the context of the given worklets.  

Respond strictly in JSON format as shown below:

{{
    "worklets": [
        {{
            "Problem Statement": "...",
            "Goal": "...",
            "Expectations": "...",
            "Training/Prerequisite": "..."
        }}
    ]
}}

Now, **generate 5 well-structured and distinct worklets** following these guidelines.""")

async def generate_worklets(worklet_data):
    prompt_template = get_prompt_template()  # Fetch the latest template dynamically
    prompt = prompt_template.format(worklet_data=worklet_data)
    generated_worklets = llm.invoke(prompt)
    print("*********************************************************************************************************************************************************************************************************************************************************************************")
    print("generated_worklets.content\n")
    print(generated_worklets.content)
    print("generated_worklets.json()\n")
    print(generated_worklets.json())
    print("generated_worklets.\n")
    print(generated_worklets)


    # return extract_json_from_llm_response(generated_worklets.content)
    return generated_worklets.content