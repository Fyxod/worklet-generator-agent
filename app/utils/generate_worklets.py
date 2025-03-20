from langchain.prompts import ChatPromptTemplate
from app.llm import llm
from app.utils.llm_response_parser import extract_json_from_llm_response


def get_prompt_template_V1():
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


def get_prompt_template_V2():
    return ChatPromptTemplate.from_template("""You are an expert in analyzing and generating structured worklet ideas. Your task is to generate **five new worklets** based on the provided examples.

### 🔹 **Instructions:**
- Ensure that the new worklets are **unique yet thematically aligned** with the given worklets.
- **Follow the exact format** below for each new worklet.
- **Ensure ideas are innovative yet practically implementable.**
- **Exclude specific names of people, organizations, or brands.**

---

### ** Structure of Each Worklet Idea:**
1. **Problem Statement**: Clearly describe the problem this worklet aims to address.
2. **Goal**: Define the objective and intended outcome.
3. **Expectations**: Describe what participants are expected to do or accomplish.
4. **Training/Prerequisite**: List any required knowledge, skills, or prior learning needed.
5. **Difficulty (1-10)**: Rate the complexity of this worklet on a scale from 1 (very easy) to 10 (very challenging).
6. **Reference Work**: Provide a relevant book, article, research paper, or online resource to help participants get started.

---

### ** Existing Worklets for Reference:**
{worklet_data}

---

### ** Additional Guidelines:**
✅ **Ensure originality**—new worklets should be inspired by, but not directly derivative of, the provided examples.  
✅ **Introduce fresh perspectives**—each worklet should offer a unique angle or approach.  
✅ **Maintain structured clarity**—ideas should be easy to understand and apply.  
✅ **Stick to the context**—avoid introducing unrelated topics.  

Respond **strictly in JSON format** as shown below:

```json
{{
    "worklets": [
        {{
            "Problem Statement": "...",
            "Goal": "...",
            "Expectations": "...",
            "Training/Prerequisite": "...",
            "Difficulty": 5,
            "Reference Work": "Book Title / Article Name / Online Course URL"
        }},
        {{
            "Problem Statement": "...",
            "Goal": "...",
            "Expectations": "...",
            "Training/Prerequisite": "...",
            "Difficulty": 3,
            "Reference Work": "Relevant research paper / Blog post link"
        }},
        {{
            "Problem Statement": "...",
            "Goal": "...",
            "Expectations": "...",
            "Training/Prerequisite": "...",
            "Difficulty": 8,
            "Reference Work": "Online tutorial / Industry report"
        }},
        {{
            "Problem Statement": "...",
            "Goal": "...",
            "Expectations": "...",
            "Training/Prerequisite": "...",
            "Difficulty": 6,
            "Reference Work": "Documentation link / Workshop recording"
        }},
        {{
            "Problem Statement": "...",
            "Goal": "...",
            "Expectations": "...",
            "Training/Prerequisite": "...",
            "Difficulty": 9,
            "Reference Work": "Academic journal / Advanced technical guide"
        }}
    ]
}}
Now, **generate 5 well-structured and distinct worklets** following these guidelines.
""")


async def generate_worklets(worklet_data):
    prompt_template = get_prompt_template_V2()  # Fetch the latest template dynamically
    prompt = prompt_template.format(worklet_data=worklet_data)
    generated_worklets = llm.invoke(prompt)
    
    return extract_json_from_llm_response([generated_worklets.content])