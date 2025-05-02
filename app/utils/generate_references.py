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
        keyword = await getKeyword(title, model)  # Await the async function
    except Exception as e:
        print(f"Error in getKeyword: {e}, using title as keyword")
        keyword = title

    with ThreadPoolExecutor() as executor:
        # Run blocking I/O operations in parallel using ThreadPoolExecutor
        loop = asyncio.get_running_loop()
        github_future = loop.run_in_executor(None, get_github_references, keyword)
        scholar_future = loop.run_in_executor(None, get_google_scholar_references, keyword)

        githubReferences, googleScholarReferences = await asyncio.gather(github_future, scholar_future)
        googleReferences = []

        if len(googleScholarReferences) == 0:
            await asyncio.sleep(5)  # Non-blocking sleep to prevent freezing the event loop
            googleScholarReferences = get_google_scholar_references(keyword)

        if len(googleScholarReferences) == 0:
            googleReferences = search_references(keyword, max_results=10)

        print(f"generated {len(githubReferences)} github references for {title}")
        print(f"generated {len(googleScholarReferences)} google scholar references for {title}")
        print(f"generated {len(googleReferences)} search engine references for {title}")

    response = []
    response.extend(googleScholarReferences)
    response.extend(githubReferences)
    response.extend(googleReferences)

    try:
        with open("final_search.json", "w") as f:
            json.dump(response, f, indent=4)
    except Exception as e:
        print(f"Failed to write results to file. Error: {e}")
    print("Final search results saved to ", response)
    return response


# getReferenceWork("Job Scheduling with AWS DynamoDB and Spring Reactive Framework", "gemma3:27b")


async def getKeyword(title, model):
    print("Inside getKeyword", title)
    prompt = arcive_temp().format(title=title)
    response = await invoke_llm(prompt, model)
    return response

# getReferenceWork("Job Scheduling with AWS DynamoDB and Spring Reactive Framework", "gemma3:27b")
# print(getKeyword("Job Scheduling with AWS DynamoDB and Spring Reactive Framework", "deepseek-r1:70b"))
# def getReferenceWorkOld(title, model):
#     """
#     Fetches reference papers from arXiv based on a keyword derived from the title.
#     Returns a list of dictionaries with title and pdf link, or an empty list on failure.
#     """
#     # print("Inside reference work", title)
    
#     try:
#         keyword = getKeyword(title, model)
#         url = f"http://export.arxiv.org/api/query?search_query=all:{keyword}"

#         headers = {
#             'User-Agent': 'MyApp/1.0 (Contact: your-email@example.com)'  # replace with your actual contact
#         }

#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()

#         root = ET.fromstring(response.content)
#         ns = {'atom': 'http://www.w3.org/2005/Atom'}

#         reference_work = []
#         for entry in root.findall('atom:entry', ns):
#             entry_title = entry.find('atom:title', ns).text 
#             pdf_link = None

#             for link in entry.findall('atom:link', ns):
#                 if link.get('title') == 'pdf':
#                     pdf_link = link.get('href')
#                     break 

#             if pdf_link:
#                 reference_work.append({"title": entry_title, "link": pdf_link})
        
#         return reference_work

#     except Exception as e:
#         print(f"Error in getReferenceWork: {e}")
#         return []