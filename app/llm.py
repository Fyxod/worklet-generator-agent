from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import os
import json
import re
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

ollama_models = [
    "gemma3:27b",
    "gemma3:latest",
    "deepseek-r1:70b",
    "llama3.3:latest"
]

def invoke_llm(prompt, model):

    raw_text = ""
    if model in ollama_models:
        print("Using Ollama")
        payload = {"prompt": prompt}
        url = f"{os.getenv('LLM_URL')}/query?model={model}"
        response = requests.post(url, json=payload)

        # Parse response JSON
        data = json.loads(response.content)
        raw_text = data.get("content", "")


        return cleaned

    else:
        print("Using Google Gemini")
        response = llm.invoke(prompt)
        raw_text = response.content
    # Clean: remove markdown symbols and normalize whitespace
    cleaned = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"\*+", "", cleaned)  # remove markdown asterisks
    cleaned = re.sub(r"#", "", cleaned)  # Remove hash symbols
    cleaned = re.sub(r"\s+", " ", cleaned) # normalize whitespace  # Normalize all whitespace
    cleaned = cleaned.strip()

    return cleaned

print(invoke_llm("what is the capital of france", "llama3.3:latest"))
