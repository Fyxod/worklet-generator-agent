from langchain.prompts import ChatPromptTemplate
from app.llm import llm
from app.utils.llm_response_parser import extract_json_from_llm_response
from langchain.schema.messages import HumanMessage

def get_prompt_template_V2():
    return ChatPromptTemplate.from_template("""You are an expert in analyzing and generating structured worklet ideas. Your task is to generate **five new worklets** based on the provided examples.

### **Instructions:**
- Ensure that the new worklets are **unique yet thematically aligned** with the given worklets.
- **Follow the exact format** below for each new worklet.
- **Ensure ideas are innovative yet practically implementable.**
- **Exclude specific names of people, organizations, or brands.**

---

### ** Structure of Each Worklet Idea:**
1. **Title**: A concise and engaging title summarizing the worklet not more than 4-6 words.
2. **Problem Statement**: Clearly describe the problem this worklet aims to address. between 28-33 words
3. **Goal**: Define the objective and intended outcome. between 30 -35 words 
4. **Expectations**: Describe what participants are expected to do or accomplish.  between 38 to 45 words 
5. **Training/Prerequisite**: List any required knowledge, skills, or prior learning needed.
6. **Difficulty (1-10)**: Rate the complexity of this worklet on a scale from 1 (very easy) to 10 (very challenging).
7. **Reference Work**: Include at least one reference work, preferably an academic or research paper. If two strong references are available, include both

---

### ** Existing Worklets for Reference:**
{worklet_data}

---

### ** Additional Guidelines:**
**Ensure originality**—new worklets should be inspired by, but not directly derivative of, the provided examples.  
**Introduce fresh perspectives**—each worklet should offer a unique angle or approach.  
**Maintain structured clarity**—ideas should be easy to understand and apply.  
**Stick to the context**—avoid introducing unrelated topics. 
**Word Limit**- Strictly adhere to word limits to avoid formatting errors in PDF generation.   

Respond **strictly in JSON format** as shown below:

```json
{{
    "worklets": [
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 5,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "http://arxiv.org/pdf/......."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }},
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 3,
            "Reference Work":[
                                    {{
                                        "title": "..................",
                                        "link": "http://arxiv.org/pdf/......."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }},
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 8,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "http://arxiv.org/pdf/......."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 6,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "http://arxiv.org/pdf/......."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }},
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 9,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "http://arxiv.org/pdf/......."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }}
    ]
}}
Now, **generate 5 well-structured and distinct worklets** following these guidelines.
""")




async def generate_worklets(worklet_data):
    prompt_template = get_prompt_template_V2()  # Fetch the latest template dynamically
    prompt = prompt_template.format(worklet_data=worklet_data)
    generated_worklets = llm.invoke(prompt)
    # generated_worklets = llm.invoke([HumanMessage(content=prompt)])
    
    return extract_json_from_llm_response([generated_worklets.content])