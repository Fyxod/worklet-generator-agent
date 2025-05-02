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
    google_api_key = os.getenv("GOOGLE_API_KEY_gemini"),
)

llm2 = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=1,
    google_api_key = os.getenv("GOOGLE_API_KEY_gemini2"),
)

ollama_models = [
    "gemma3:27b",
]

def invoke_llm(prompt, model):
    raw_text = ""
    max_retries = 4

    if model in ollama_models:
        payload = {"prompt": prompt}
        url = f"{os.getenv('LLM_URL')}/query?model={model}"

        for attempt in range(max_retries):
            response = None
            try:
                response = requests.post(url, json=payload)
                if response.status_code != 200:
                    time.sleep(8)
                    continue

                data = json.loads(response.content)
                raw_text = data.get("content", "")
                break  # Success, exit the loop

            except json.JSONDecodeError: 
                time.sleep(20)

        if not raw_text:
            return "LLM failed after 4 attempts."

    else:
        response = llm.invoke(prompt)
        raw_text = response.content

    cleaned = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"\*+", "", cleaned)     # Remove markdown asterisks
    cleaned = re.sub(r"#", "", cleaned)       # Remove hash symbols
    cleaned = re.sub(r"\s+", " ", cleaned)    # Normalize whitespace
    cleaned = cleaned.replace('")', '"')
    if '`' in cleaned:
        cleaned = cleaned[cleaned.find('`'):]
    cleaned = cleaned.strip()
    cleaned =cleaned.replace("```json", "").replace("```", "").strip()
    return cleaned
