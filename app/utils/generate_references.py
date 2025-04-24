import requests
from langchain.prompts import ChatPromptTemplate
import xml.etree.ElementTree as ET
from app.llm import llm, invoke_llm
# from llm import llm
from langchain.schema.messages import HumanMessage
from app.utils.reference_functions.github import get_github_references
from app.utils.reference_functions.google_scholar import get_google_scholar_references
# from reference_functions.github import get_github_references
# from reference_functions.google_scholar import get_google_scholar_references
from concurrent.futures import ThreadPoolExecutor

prompt_template = ChatPromptTemplate.from_template(
    """
    Only output the keyword/phrase for arXiv search based on this topic: '{title}'. No preamble. No commentary. No punctuation. Just the keyword or phrase.
    Example outputs : 
    1. Input - Self supervised Multi-turn dialog emotion recognition | Output - self-supervised dialog emotion
    2. Input - Language Agnostic Large Language Model | Output - Multilingual LLM
    3. Input - Network FCAPS Correlation using LLM | Output - LLM FCAPS correlation
    4. Input - Deep Packet Inspection Traffic Visualization | Output - Deep Packet Inspection
    5. Input - Real Time Call Video Anti Aliasing | Output - anti-aliasing
    """
)
# prompt_template = ChatPromptTemplate.from_template(
#     """
#     I want you to strictly just give me a keyword to search in arxiv api to get me the research papers best suited for the following topic - {title}. Just give me the keyword as the answer and no other extra stuff
#     """
# )

def getReferenceWork(title, model):
    keyword = getKeyword(title, model)

    with ThreadPoolExecutor() as executor:
        future_github = executor.submit(get_github_references, keyword)
        future_scholar = executor.submit(get_google_scholar_references, keyword)

        githubReferences = future_github.result()
        googleScholarReferences = future_scholar.result()

    response = []
    response.extend(githubReferences)
    print("Github references", githubReferences)
    response.extend(googleScholarReferences)
    print(response)
    return response


def getKeyword(title, model):
    print("Inside getKeyword ", title)
    prompt = prompt_template.format(title=title)
    # print("printing prompt", prompt)
    # prompt = prompt_template.format_prompt(title=title).to_string()
    response = invoke_llm(prompt, model)
    # response = llm.invoke(prompt)
    print("printing keyword", response)
    # response = llm.invoke([HumanMessage(content=prompt)])
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