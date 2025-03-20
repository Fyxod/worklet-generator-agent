from langchain.prompts import ChatPromptTemplate
from app.llm import llm

# Prompt can be improved much more
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{worklet_data}

---

Generate 5 new worklet ideas based on the above worklet ideas. Ignore the names of the people and just focus on the ideas.
"""

prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

async def generate_worklets(worklet_data: str):
    prompt = prompt_template.format(worklet_data=worklet_data)
    generated_worklets = llm.invoke(prompt)
    return generated_worklets

