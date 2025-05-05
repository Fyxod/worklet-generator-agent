import requests
from langchain.prompts import ChatPromptTemplate
import xml.etree.ElementTree as ET
from app.llm import invoke_llm
from langchain.schema.messages import HumanMessage
from app.utils.reference_functions.github import get_github_references
from app.utils.reference_functions.google_scholar import get_google_scholar_references
from app.utils.search_functions.search import search_references
from concurrent.futures import ThreadPoolExecutor
from app.utils.prompt_templates import arcive_temp
from time import sleep
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def getReferenceWork(title, model="gemma3:27b"):
    keyword = ""
    try:
        keyword = await getKeyword(title, model)
    except Exception as e:
        keyword = title

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        github_future = loop.run_in_executor(None, get_github_references, keyword)
        scholar_future = loop.run_in_executor(None, get_google_scholar_references, keyword)

        githubReferences, googleScholarReferences = await asyncio.gather(github_future, scholar_future)
        googleReferences = []

        if len(googleScholarReferences) == 0:
            await asyncio.sleep(5)
            googleScholarReferences = get_google_scholar_references(keyword)

        if len(googleScholarReferences) == 0:
            googleReferences = search_references(keyword, max_results=10)

    response = []
    response.extend(googleScholarReferences)
    response.extend(githubReferences)
    response.extend(googleReferences)

    return response

async def getKeyword(title, model):
    prompt = arcive_temp().format(title=title)
    response = await invoke_llm(prompt, model)
    return response
