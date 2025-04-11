from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import os
import json
import re
import time
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

ollama_models = [
    "gemma3:27b",
    "gemma3:latest",
    "deepseek-r1:70b",
    "llama3.3:latest"
]

def invoke_llm(prompt, model):
    raw_text = ""
    max_retries = 3

    if model in ollama_models:
        print("Using Ollama")
        payload = {"prompt": prompt}
        url = f"{os.getenv('LLM_URL')}/query?model={model}"

        for attempt in range(max_retries):
            try:
                response = requests.post(url, json=payload)

                if response.status_code != 200:
                    print(f"Attempt {attempt+1}: Error {response.status_code} - {response.text}")
                    time.sleep(1)
                    continue

                data = json.loads(response.content)
                raw_text = data.get("content", "")
                break  # Success, exit the loop

            except json.JSONDecodeError:
                print(f"Attempt {attempt+1}: Failed to decode JSON - {response.content}")
                time.sleep(1)

        if not raw_text:
            return "LLM failed after 3 attempts."

    else:
        print("Using Google Gemini")
        response = llm.invoke(prompt)
        raw_text = response.content

    # Clean: remove markdown symbols and normalize whitespace
    cleaned = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"\*+", "", cleaned)     # Remove markdown asterisks
    cleaned = re.sub(r"#", "", cleaned)       # Remove hash symbols
    cleaned = re.sub(r"\s+", " ", cleaned)    # Normalize whitespace
    cleaned = cleaned.strip()

    return cleaned

# print(invoke_llm("write a 100 word essay on trees", "llama3.3:latest"))
