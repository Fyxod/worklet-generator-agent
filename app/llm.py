from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=1,
    google_api_key = os.getenv("GOOGLE_API_KEY"),
)

llm2 = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=1,
    google_api_key = os.getenv("GOOGLE_API_KEY2"),
)

# from langchain_community.chat_models import ChatOllama
# from langchain.schema.messages import HumanMessage
# from langchain_ollama import ChatOllama

# # Create the LLM instance using Ollama with the 'mistral' model
# llm = ChatOllama(model="mistral", temperature=1)

# Example prompt
# response = llm.invoke([HumanMessage(content="What is the capital of France?")])
# print(response.content)










# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os
# import requests

# load_dotenv()

# # llm_switch = "gemini"
# llm_switch = "ollama"
# model = "gemma3:27b"

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=1,
#     google_api_key = os.getenv("GOOGLE_API_KEY"),
# )

# llm2 = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=1,
#     google_api_key = os.getenv("GOOGLE_API_KEY2"),
# )

# # from langchain_community.chat_models import ChatOllama
# # from langchain.schema.messages import HumanMessage
# # from langchain_ollama import ChatOllama

# # # Create the LLM instance using Ollama with the 'mistral' model
# # llm = ChatOllama(model="mistral", temperature=1)

# # Example prompt
# # response = llm.invoke([HumanMessage(content="What is the capital of France?")])
# # print(response.content)



# def invoke_llm(prompt, model):

#     if llm_switch == "ollama":
#         payload = {"prompt": prompt}
#         url = f"{os.getenv('LLM_URL')}/query?model={model}"
#         response = requests.post(url, json=payload) 
#         return{"content":response.json()['content'].strip()}

#     elif llm_switch == "gemini":
#         response = llm.invoke(prompt)
#         return response

# # print(invoke_llm("What is the capital of France?"))
